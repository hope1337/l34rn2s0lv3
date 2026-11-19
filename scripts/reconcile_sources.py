#!/usr/bin/env python3
"""Rebuild the canonical source registry from preserved retrieval logs."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    records, seen = [], set()
    for path in sorted((ROOT / 'catalog/sources').glob('*-log.json')):
        for record in json.loads(path.read_text(encoding='utf-8')):
            if record['id'] in seen:
                raise ValueError(f'Duplicate source ID {record["id"]}: assign a new dated ID to a refresh')
            records.append(record)
            seen.add(record['id'])
    output = ROOT / 'catalog/sources/registry.json'
    output.write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Reconciled {len(records)} source records')


if __name__ == '__main__':
    main()
