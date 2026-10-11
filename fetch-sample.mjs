// Node >=22. Download the pinned sample, or verify a supplied local JSONL file.
import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
const url = 'https://huggingface.co/datasets/pranasara-intelligence-lab/sleep-discovery-sample/resolve/6e62f6614cfebfdb1b319a0f081e24ba46e27f87/sleep-discovery.jsonl';
const sha256 = '1db7da5e2d54812b5ce9eee93615f2f8815e6e9d529bc69cd1b2cdabbdf521d3';
if (process.argv.length > 3) throw new Error('Usage: node fetch-sample.mjs [local.jsonl]');
let payload;
if (process.argv[2]) {
  payload = await readFile(process.argv[2]);
} else {
  const response = await fetch(url, { signal: AbortSignal.timeout(30000) });
  if (!response.ok) throw new Error(`Download failed: HTTP ${response.status}`);
  if (!response.url.startsWith('https://')) throw new Error('Refusing non-HTTPS redirect');
  payload = Buffer.from(await response.arrayBuffer());
}
if (createHash('sha256').update(payload).digest('hex') !== sha256) throw new Error('Checksum mismatch; refusing to load sample');
const records = payload.toString('utf8').trimEnd().split('\n').map(line => JSON.parse(line));
if (records.length !== 39) throw new Error('Expected 39 records');
console.log(`PASS: ${records.length} records; pinned SHA256 verified`);
console.log(JSON.stringify(records[0], null, 2));
