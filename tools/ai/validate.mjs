#!/usr/bin/env node
// G0 gate CLI. Usage: node tools/ai/validate.mjs [file ...]
// Without arguments it checks every contract and ticket under .ai/.
// Needs the tool dependencies once: npm ci --prefix tools
import { validate } from './contracts.mjs';

const { errors, checked } = validate(process.argv.slice(2));
if (errors.length) {
  console.error(`G0 failed: ${errors.length} problem(s) in ${checked} file(s)`);
  for (const e of errors) console.error(`  - ${e}`);
  process.exit(1);
}
console.log(`G0 passed: ${checked} file(s) checked`);
