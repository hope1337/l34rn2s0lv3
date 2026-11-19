#!/usr/bin/env python3
"""Validate, search and export the evidence-backed competition catalog (offline)."""
import argparse
import csv
import hashlib
import json
import re
import sqlite3
import sys
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
WEIGHTS = dict(task_evaluation=15, solution_depth=20, public_code=20,
               dataset_access=15, technical_value=15, transfer_value=10, result_trust=5)


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def safe_path(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes repository: {relative}')
    return path


def canonical_url(url):
    p = urlsplit(url)
    # Query can identify an evaluation version: preserve it. Only trim fragment/trailing slash.
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path.rstrip('/'), p.query, ''))


def identity_key(record):
    i = record['identity']
    return (i['platform'].casefold(), canonical_url(i['canonical_url']),
            i['year'], i['track'], i['evaluation_version'])


def score_record(rating):
    points = [rating['criteria'][key]['points'] for key in WEIGHTS]
    if any(p is None for p in points):
        return None, 'UNRATED'
    total = sum(points)
    return total, 'A' if total >= 80 else 'B' if total >= 60 else 'C'


def load_records(root=ROOT):
    return [(path, read(path)) for folder in ['discovery', 'curated']
            for path in sorted((root / 'catalog' / folder).glob('*.json'))]


def check_schema(obj, schema, label, errors):
    for error in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(obj):
        loc = '/'.join(map(str, error.absolute_path))
        errors.append(f'{label}:{loc}: {error.message}')


def validate(root=ROOT):
    errors = []
    schema = read(root / 'schemas/competition.schema.json')
    eschema = read(root / 'schemas/evidence.schema.json')
    sources = read(root / 'catalog/sources/registry.json')
    source_schema = root / 'schemas/source.schema.json'
    if source_schema.exists():
        check_schema(sources, read(source_schema), 'catalog/sources/registry.json', errors)
        if errors:
            return errors
    source_map = {}
    for s in sources:
        sid = s.get('id')
        if sid in source_map:
            errors.append(f'duplicate source ID: {sid}')
        source_map[sid] = s
        if s.get('status') == 'retrieved':
            try:
                path = safe_path(root, s['snapshot'])
                if hashlib.sha256(path.read_bytes()).hexdigest() != s['sha256']:
                    errors.append(f'{sid}: snapshot hash mismatch')
            except (KeyError, OSError, ValueError) as exc:
                errors.append(f'{sid}: {exc}')

    def refs(ids, label, require_retrieved=False):
        for sid in ids:
            if sid not in source_map:
                errors.append(f'{label}: unknown source {sid}')
            elif require_retrieved and source_map[sid].get('status') != 'retrieved':
                errors.append(f'{label}: VERIFIED requires a retrieved source: {sid}')

    seen_ids, seen_keys = set(), {}
    for path, r in load_records(root):
        label = str(path.relative_to(root))
        before = len(errors)
        check_schema(r, schema, label, errors)
        if len(errors) != before:
            continue  # Structural errors are already actionable; avoid cascaded KeyErrors.
        if path.stem != r['id']:
            errors.append(f'{label}: filename must match ID')
        if r['id'] in seen_ids:
            errors.append(f'{label}: duplicate ID')
        seen_ids.add(r['id'])
        key = identity_key(r)
        if key in seen_keys:
            errors.append(f'{label}: duplicate identity with {seen_keys[key]}')
        seen_keys[key] = r['id']
        refs(r['source_ids'], label)
        refs(r['identity']['source_ids'], label)
        refs(r['lifecycle']['source_ids'], label)
        refs(r['task']['source_ids'], label, r['task']['status'] == 'VERIFIED')
        if r['task']['status'] == 'VERIFIED' and not r['task']['source_ids']:
            errors.append(f'{label}: verified task requires evidence')
        for name, fact in r['availability'].items():
            refs(fact['source_ids'], f'{label}:{name}', fact['status'] == 'verified')
            if fact['status'] == 'verified' and (fact['value'] is None or not fact['source_ids']):
                errors.append(f'{label}:{name}: verified fact needs value and source')
            if fact['status'] in ['unknown', 'not_checked', 'blocked'] and fact['value'] is not None:
                errors.append(f'{label}:{name}: unresolved fact value must be null')
        rating = r['curation']['rating']
        for name, criterion in rating['criteria'].items():
            p = criterion['points']
            refs(criterion['source_ids'], f'{label}:rating:{name}', p is not None)
            if p is not None:
                if not criterion['source_ids'] or p not in [WEIGHTS[name] * v for v in [0, .25, .5, .75, 1]]:
                    errors.append(f'{label}:{name}: invalid points or missing evidence')
        total, tier = score_record(rating)
        if total != rating['total'] or tier != rating['tier']:
            errors.append(f'{label}: rating total/tier inconsistent (expected {total}/{tier})')
        if path.parent.name != r['curation']['state']:
            errors.append(f'{label}: state must match catalog directory')
        if r['curation']['state'] == 'curated':
            if r['identity']['year'] is None or r['identity']['track'] is None:
                errors.append(f'{label}: curated identity needs year and track')
            if r['task']['status'] != 'VERIFIED' or r['availability']['final_results']['status'] != 'verified':
                errors.append(f'{label}: curated needs verified task and final results')
            if not any(r['availability'][k]['status'] == 'verified' for k in ['code', 'writeups']):
                errors.append(f'{label}: curated needs a verified solution source')
        if r['research']['report_path']:
            try:
                if not safe_path(root, r['research']['report_path']).is_file():
                    errors.append(f'{label}: missing report')
            except ValueError as exc:
                errors.append(f'{label}: {exc}')

    all_claim_ids = set()
    for path in sorted((root / 'competitions').glob('*/evidence.json')):
        claims = read(path)
        check_schema(claims, eschema, str(path.relative_to(root)), errors)
        if not isinstance(claims, list):
            continue
        for c in claims:
            if not isinstance(c, dict) or not all(k in c for k in ['id', 'status', 'source_ids']):
                continue
            if c['id'] in all_claim_ids:
                errors.append(f'duplicate claim ID: {c["id"]}')
            all_claim_ids.add(c['id'])
            refs(c['source_ids'], c['id'], c['status'] == 'VERIFIED')
            if c['status'] == 'VERIFIED' and (not c['source_ids'] or not c.get('locator')):
                errors.append(f'{c["id"]}: verified claim needs source and locator')
            if c['status'] == 'INFERRED' and (not c.get('assumptions') or not c.get('test')):
                errors.append(f'{c["id"]}: inferred claim needs assumptions and test')
            if c.get('scope') == 'measured' and not c.get('artifact'):
                errors.append(f'{c["id"]}: measured claim needs artifact')
            if c.get('artifact'):
                try:
                    if not safe_path(root, c['artifact']).is_file():
                        errors.append(f'{c["id"]}: missing measurement artifact')
                except ValueError as exc:
                    errors.append(f'{c["id"]}: {exc}')
        # Catch orphaned prose citations when a claim ID is renamed/deleted.
        known = {c.get('id') for c in claims if isinstance(c, dict)}
        for name in ['report.md', 'pipeline.md']:
            prose = path.parent / name
            if prose.exists():
                for block in re.findall(r'\[([^\]\n]+)\](?!\()', prose.read_text(encoding='utf-8')):
                    if block.startswith(('cold-', 'bloom-', 'memes-')):
                        for claim_id in block.split(';'):
                            if claim_id.strip() not in known:
                                errors.append(f'{prose.name}: missing claim citation {claim_id.strip()}')
    state_schema = root / 'schemas/research-state.schema.json'
    if state_schema.exists():
        state_contract = read(state_schema)
        for path in sorted((root / 'competitions').glob('*/state.json')):
            state = read(path)
            check_schema(state, state_contract, str(path.relative_to(root)), errors)
            if state.get('competition_id') != path.parent.name:
                errors.append(f'{path}: state competition ID mismatch')
            for artifact in state.get('artifacts', []):
                try:
                    if not safe_path(path.parent, artifact).is_file():
                        errors.append(f'{path}: missing state artifact {artifact}')
                except ValueError as exc:
                    errors.append(f'{path}: {exc}')
            if state.get('overall_status') == 'complete' and (state.get('unknowns') or any(
                    m.get('status') in ['partial', 'blocked'] for m in state.get('modules', {}).values())):
                errors.append(f'{path}: complete state has unresolved required work')
    cards_path = root / 'techniques/knowledge_cards.json'
    if cards_path.exists():
        cards = read(cards_path)
        seen_cards = set()
        for card in cards:
            cid = card.get('id')
            if cid in seen_cards:
                errors.append(f'duplicate knowledge card ID: {cid}')
            seen_cards.add(cid)
            for claim_id in card.get('claim_ids', []):
                if claim_id not in all_claim_ids:
                    errors.append(f'{cid}: unknown knowledge evidence claim {claim_id}')
            if not card.get('claim_ids') or not card.get('when_to_use') or not card.get('failure_modes'):
                errors.append(f'{cid}: knowledge card needs evidence, conditions and failure modes')
    return errors


def matches(r, args):
    fields = [r['title'], *r['aliases'], r['task']['name'] or '', r['identity']['organizer'] or '', *r['tags']]
    return (not args.query or args.query.casefold() in ' '.join(fields).casefold()) and all([
        not args.modality or args.modality in r['task']['modalities'],
        not args.task or args.task.casefold() in (r['task']['name'] or '').casefold(),
        not args.year or args.year == r['identity']['year'],
        not args.platform or args.platform.casefold() == r['identity']['platform'].casefold(),
        not args.state or args.state == r['curation']['state'],
        not args.tier or args.tier == r['curation']['rating']['tier'],
        not args.code or args.code == r['availability']['code']['status'],
        not args.data or args.data == r['availability']['data']['status'],
        not args.status or args.status == r['research']['status'],
    ])


def build(root=ROOT):
    records = [r for _, r in load_records(root)]
    target = root / 'catalog/indexes'
    target.mkdir(parents=True, exist_ok=True)
    columns = ['id', 'title', 'platform', 'year', 'track', 'task', 'modalities', 'state', 'tier', 'score', 'code', 'data', 'research_status', 'url']
    rows = []
    for r in records:
        i, t, c, a = r['identity'], r['task'], r['curation'], r['availability']
        rows.append([r['id'], r['title'], i['platform'], i['year'], i['track'], t['name'],
                     '|'.join(t['modalities']), c['state'], c['rating']['tier'], c['rating']['total'],
                     a['code']['status'], a['data']['status'], r['research']['status'], i['canonical_url']])
    with (target / 'competitions.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)
    def md(value):
        return str(value if value is not None else '—').replace('|', ',').replace('\n', ' ')
    lines = ['# Competition catalog', '', f'{len(records)} records. Generated by `python3 scripts/lab.py build`. Discovery chưa đồng nghĩa đã audit.', '',
             '| Competition | Year / track | Modality | State | Tier | Research |', '|---|---|---|---|---|---|']
    for r in records:
        lines.append(f'| [{md(r["title"])}](../{r["curation"]["state"]}/{r["id"]}.json) | {md(r["identity"]["year"])} / {md(r["identity"]["track"])} | {md(", ".join(r["task"]["modalities"]))} | {r["curation"]["state"]} | {r["curation"]["rating"]["tier"]} | {r["research"]["status"]} |')
    (target / 'competitions.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    with sqlite3.connect(target / 'catalog.sqlite') as db:
        db.execute('DROP TABLE IF EXISTS competitions')
        db.execute('CREATE TABLE competitions (id TEXT PRIMARY KEY, title TEXT, platform TEXT, year INTEGER, track TEXT, task TEXT, modalities TEXT, state TEXT, tier TEXT, score REAL, code TEXT, data TEXT, research_status TEXT, url TEXT, record_json TEXT)')
        db.executemany('INSERT INTO competitions VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                       [row + [json.dumps(r, ensure_ascii=False)] for row, r in zip(rows, records)])
    return len(records)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('validate')
    sub.add_parser('build')
    search = sub.add_parser('search')
    for field in ['query', 'task', 'modality', 'platform', 'state', 'tier', 'code', 'data', 'status']:
        search.add_argument('--' + field)
    search.add_argument('--year', type=int)
    args = p.parse_args()
    errors = validate()
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    if args.command == 'validate':
        print(f'PASS: {len(load_records())} competitions; schemas, evidence references, identity, scores and snapshot hashes valid')
    elif args.command == 'build':
        print(f'Built {build()} records into Markdown, CSV and SQLite')
    else:
        found = [r for _, r in load_records() if matches(r, args)]
        print(json.dumps(found, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
