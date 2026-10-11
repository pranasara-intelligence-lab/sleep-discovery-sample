#!/bin/sh
# Download only; use the supplied validator to check count and pinned checksum.
set -eu
if [ "$#" -ne 1 ]; then
  printf '%s\n' 'Usage: sh fetch-sample.sh /path/to/output.jsonl' >&2
  exit 2
fi
curl --fail --show-error --location --proto '=https' --proto-redir '=https' --connect-timeout 15 --max-time 60 \
  --output "$1" \
  'https://huggingface.co/datasets/pranasara-intelligence-lab/sleep-discovery-sample/resolve/6e62f6614cfebfdb1b319a0f081e24ba46e27f87/sleep-discovery.jsonl'
printf '%s\n' 'Download complete. Validate with: python3 load-sample.py /path/to/output.jsonl (use your selected output path).'
