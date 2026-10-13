// G0 gate: checks the .ai/ contract and ticket files against their JSON Schemas,
// plus the cross-checks a schema cannot express (frame order, file references, evidence).
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { basename, dirname, join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import Ajv from 'ajv';
import { parse } from 'yaml';

export const repo = resolve(dirname(fileURLToPath(import.meta.url)), '..', '..');
const aiDir = join(repo, '.ai');
const schemaDir = join(aiDir, 'schemas');

// Which schema each file under .ai/ must follow, by repository-relative path.
const RULES = [
  { match: /^\.ai\/contracts\/versions\.ya?ml$/, schema: 'versions' },
  { match: /^\.ai\/contracts\/art-bible\.ya?ml$/, schema: 'art-bible' },
  { match: /^\.ai\/contracts\/perf-budget\.ya?ml$/, schema: 'perf-budget' },
  { match: /^\.ai\/contracts\/bosses\/[^/]+\.ya?ml$/, schema: 'boss', check: checkBoss },
  { match: /^\.ai\/tickets\/[^/]+\.ya?ml$/, schema: 'ticket', check: checkTicket },
];

export const toRel = (file) => relative(repo, resolve(file)).split(sep).join('/');

let ajv;
const compiled = new Map();
function loadSchemas(errors) {
  ajv = new Ajv({ allErrors: true });
  compiled.clear();
  // Compile every schema up front so a broken one is reported even if no file uses it.
  for (const name of readdirSync(schemaDir).filter((f) => f.endsWith('.schema.json'))) {
    try {
      compiled.set(name.replace('.schema.json', ''), ajv.compile(JSON.parse(readFileSync(join(schemaDir, name), 'utf8'))));
    } catch (err) {
      errors.push(`.ai/schemas/${name}: ${err.message}`);
    }
  }
}

function listFiles(dir) {
  if (!existsSync(dir)) return [];
  return readdirSync(dir).flatMap((name) => {
    const full = join(dir, name);
    return statSync(full).isDirectory() ? listFiles(full) : [full];
  });
}

function checkBoss(data, rel, errors) {
  const seen = new Set();
  for (const move of data.moves ?? []) {
    if (seen.has(move.id)) errors.push(`${rel}: move id "${move.id}" is used twice`);
    seen.add(move.id);
    const [start, end] = move.active_frames;
    if (start < move.telegraph_frames) {
      errors.push(`${rel}: move "${move.id}" becomes active (${start}) before its telegraph ends (${move.telegraph_frames})`);
    }
    if (end < start) errors.push(`${rel}: move "${move.id}" active_frames end (${end}) is before start (${start})`);
  }
}

function checkTicket(data, rel, errors) {
  const name = basename(rel).replace(/\.ya?ml$/, '');
  if (!name.startsWith('_') && data.id !== name) errors.push(`${rel}: id "${data.id}" must match the file name "${name}"`);
  for (const path of data.contract ?? []) {
    if (!existsSync(join(repo, path))) errors.push(`${rel}: contract file "${path}" does not exist`);
  }
  // Default-FAIL: a ticket may only claim PASS when its evidence folder holds something.
  if (data.status === 'PASS') {
    const evidence = listFiles(join(aiDir, 'evidence', data.id));
    if (evidence.length === 0) errors.push(`${rel}: status is PASS but .ai/evidence/${data.id}/ has no evidence files`);
  }
}

function checkFile(file, errors) {
  const rel = toRel(file);
  const rule = RULES.find((r) => r.match.test(rel));
  if (!rule) return false;
  let data;
  try {
    data = parse(readFileSync(file, 'utf8'));
  } catch (err) {
    errors.push(`${rel}: YAML parse error: ${err.message}`);
    return true;
  }
  const validate = compiled.get(rule.schema);
  if (!validate) {
    errors.push(`${rel}: schema "${rule.schema}" is missing from .ai/schemas/`);
    return true;
  }
  if (!validate(data)) {
    for (const e of validate.errors) errors.push(`${rel}: ${e.instancePath || '(root)'} ${e.message}`);
    return true;
  }
  rule.check?.(data, rel, errors);
  return true;
}

/** Validates the given files, or every mapped file under .ai/ when none are given. */
export function validate(files = []) {
  const errors = [];
  loadSchemas(errors);
  const targets = files.length ? files.map((f) => resolve(f)) : listFiles(aiDir);
  let checked = 0;
  for (const file of targets) if (checkFile(file, errors)) checked++;
  return { errors, checked };
}
