#!/usr/bin/env node
// Starts the Blockbench headless MCP server (stdio) with the repository's models/ folder as its root.
// It edits, validates, converts and renders .bbmodel files without Blockbench running.
//
// The pinned server is installed once into tools/mcp/.cache/ (gitignored) and then run directly
// with this Node executable. That avoids npx re-resolving the GitHub package on every start
// (slow, and on Windows it leaves locked files in the npx cache) and needs no shell to start.
// stdout is the MCP channel, so everything the installer prints goes to stderr.
import { spawn, spawnSync } from 'node:child_process';
import { existsSync, mkdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const VERSION = 'v1.10.0';
const SPEC = `github:jasonjgardner/blockbench-mcp-plugin#${VERSION}`;

const repo = resolve(dirname(fileURLToPath(import.meta.url)), '..', '..');
const root = join(repo, 'models');
const installDir = join(repo, 'tools', 'mcp', '.cache', `bbmodel-${VERSION}`);
const entry = join(installDir, 'node_modules', 'blockbench-mcp', 'bin', 'blockbench-mcp-headless.mjs');

function install() {
  mkdirSync(installDir, { recursive: true });
  process.stderr.write(`bbmodel-headless: installing ${SPEC} (first run only)...\n`);
  // npm is a .cmd shim on Windows, so it needs a shell there; one command string avoids Node's
  // warning about unescaped argument arrays. The paths come from this repository and hold no quotes.
  const command = `npm install --prefix "${installDir}" --no-audit --no-fund --loglevel=error "${SPEC}"`;
  const result = spawnSync(command, { shell: true, stdio: ['ignore', 2, 2] });
  if (result.status !== 0 || !existsSync(entry)) {
    process.stderr.write(`bbmodel-headless: install failed (exit ${result.status}). Delete ${installDir} and run again.\n`);
    process.exit(1);
  }
}

if (!existsSync(entry)) install();
mkdirSync(root, { recursive: true });

const child = spawn(process.execPath, [entry, '--root', root, ...process.argv.slice(2)], { stdio: 'inherit' });
child.on('error', (err) => {
  process.stderr.write(`bbmodel-headless: failed to start: ${err.message}\n`);
  process.exit(1);
});
child.on('exit', (code, signal) => process.exit(code ?? (signal ? 1 : 0)));
for (const sig of ['SIGINT', 'SIGTERM']) process.on(sig, () => child.kill(sig));
