#!/usr/bin/env node
// Claude Code PostToolUse hook: when Claude writes or edits a file under .ai/, re-run the G0
// check and hand any problems back to Claude next to the tool result. It stays silent for
// other files and never fails the tool call itself.
import { relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const repo = resolve(fileURLToPath(import.meta.url), '..', '..', '..');
const reply = (obj) => process.stdout.write(JSON.stringify(obj));

let input = '';
for await (const chunk of process.stdin) input += chunk;

let file;
try {
  file = JSON.parse(input)?.tool_input?.file_path;
} catch {
  process.exit(0);
}
if (!file) process.exit(0);

const rel = relative(repo, resolve(file)).split(sep).join('/');
if (!rel.startsWith('.ai/') || !/\.(ya?ml|json)$/.test(rel)) process.exit(0);

let lib;
try {
  lib = await import('./contracts.mjs');
} catch {
  reply({
    hookSpecificOutput: {
      hookEventName: 'PostToolUse',
      additionalContext: 'G0 contract check skipped: tool dependencies are not installed. Run `npm ci --prefix tools` once.',
    },
  });
  process.exit(0);
}

// A schema change can affect every file, so check everything; otherwise only the edited file.
const { errors } = rel.startsWith('.ai/schemas/') ? lib.validate() : lib.validate([file]);
if (errors.length) {
  reply({ decision: 'block', reason: `G0 contract check failed:\n${errors.map((e) => `- ${e}`).join('\n')}` });
}
