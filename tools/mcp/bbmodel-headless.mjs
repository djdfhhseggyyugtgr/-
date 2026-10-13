#!/usr/bin/env node
// Starts the Blockbench headless MCP server (stdio) with the repository's models/ folder as its root.
// It edits, validates, converts and renders .bbmodel files without Blockbench running.
// Launched through Node rather than npx directly, because Windows cannot spawn the npx .cmd shim
// without a shell, and the repository path contains spaces that need quoting there.
import { spawn } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const VERSION = 'v1.10.0';
const repo = resolve(dirname(fileURLToPath(import.meta.url)), '..', '..');
const root = join(repo, 'models');
mkdirSync(root, { recursive: true });

const isWindows = process.platform === 'win32';
const quote = (arg) => (isWindows ? `"${arg}"` : arg);
const args = ['-y', `github:jasonjgardner/blockbench-mcp-plugin#${VERSION}`, '--root', root, ...process.argv.slice(2)];

const child = spawn('npx', args.map(quote), { stdio: 'inherit', shell: isWindows });
child.on('error', (err) => {
  process.stderr.write(`bbmodel-headless: failed to start npx: ${err.message}\n`);
  process.exit(1);
});
child.on('exit', (code, signal) => process.exit(code ?? (signal ? 1 : 0)));
