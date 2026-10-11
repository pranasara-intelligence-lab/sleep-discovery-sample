#!/usr/bin/env python3
"""Load the pinned public sample, or verify a supplied local JSONL file."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

URL = 'https://huggingface.co/datasets/pranasara-intelligence-lab/sleep-discovery-sample/resolve/6e62f6614cfebfdb1b319a0f081e24ba46e27f87/sleep-discovery.jsonl'
SHA256 = '1db7da5e2d54812b5ce9eee93615f2f8815e6e9d529bc69cd1b2cdabbdf521d3'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('local_jsonl', nargs='?', type=Path)
    args = parser.parse_args()
    if args.local_jsonl:
        payload = args.local_jsonl.read_bytes()
    else:
        with urlopen(URL, timeout=30) as response:
            if not response.geturl().startswith('https://'):
                raise ValueError('Refusing non-HTTPS redirect')
            payload = response.read()
    if hashlib.sha256(payload).hexdigest() != SHA256:
        raise ValueError('Checksum mismatch; refusing to load sample')
    records = [json.loads(line) for line in payload.decode('utf-8').splitlines()]
    if len(records) != 39:
        raise ValueError('Expected 39 records')
    print(f'PASS: {len(records)} records; pinned SHA256 verified')
    print(json.dumps(records[0], ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
