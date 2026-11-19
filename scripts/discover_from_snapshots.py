#!/usr/bin/env python3
"""Conservatively import candidates from explicit organizer snapshots; never overwrite records."""
import json
import re
import unicodedata
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

from lab import ROOT, WEIGHTS


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.href, self.parts = [], None, []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.href, self.parts = dict(attrs).get('href'), []

    def handle_data(self, data):
        if self.href:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == 'a' and self.href:
            self.links.append((self.href, ' '.join(''.join(self.parts).split())))
            self.href = None


def slug(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', text).strip('-')


def infer_modalities(title):
    text = title.lower()
    found = []
    for modality, terms in {
        'time_series': ['forecast', 'energy', 'time series', 'pushback'],
        'speech': ['speech', 'speaker', 'spoken', 'asr', 'voice'],
        'audio': ['sound', 'audio', 'acoustic', 'bioacoustic', 'cough'],
        'text': ['text', 'translation', 'parsing', 'legal', 'qa', 'language', 'narrative', 'entailment', 'opinion'],
        'image': ['image', 'segmen', 'lesion', 'detection', 'visual', 'biops', 'kelp', 'whale', 'bees'],
        'satellite': ['satellite', 'flood', 'cloud', 'aerial', 'geopose', 'bioMass'],
        'video': ['video', 'tracking', 'driving', 'fish-eye'],
    }.items():
        if any(t.lower() in text for t in terms):
            found.append(modality)
    return found or ['unknown']


def record(cid, title, url, platform, sid, year=None, track=None, organizer=None):
    return {
        'schema_version': '1.0', 'id': cid, 'title': title, 'aliases': [],
        'identity': {'platform': platform, 'organizer': organizer, 'year': year, 'track': track,
                     'evaluation_version': None, 'canonical_url': url, 'source_ids': [sid]},
        'lifecycle': {'status': 'unknown', 'source_ids': [], 'note': 'Chưa audit thời gian/kết quả từng competition.'},
        'task': {'name': None, 'modalities': infer_modalities(title), 'status': 'INFERRED',
                 'source_ids': [sid], 'note': 'Modality suy từ tên; chưa xác minh task/evaluator. unknown là chưa phân loại.'},
        'availability': {k: {'status': 'not_checked', 'value': None, 'source_ids': [],
                              'note': 'Chưa audit riêng availability; không suy ra từ organizer index.'}
                         for k in ['data', 'code', 'writeups', 'final_results', 'dataset_license', 'code_license', 'checkpoints']},
        'curation': {'state': 'discovery', 'reasons': ['Candidate từ nguồn có thể truy vết; cần audit trước khi khuyến nghị.'],
                     'limitations': ['Chưa kiểm chứng riêng rules, dữ liệu, năm/track nếu null và final results.'], 'red_flags': [],
                     'rating': {'criteria': {k: {'points': None, 'source_ids': [], 'justification': 'Chưa audit tiêu chí này.'} for k in WEIGHTS},
                                'total': None, 'tier': 'UNRATED'}},
        'research': {'status': 'not_started', 'report_path': None,
                     'next_actions': ['Xác minh định danh year/track/evaluation, task, rules, final results và solution sources.']},
        'last_verified_at': None, 'source_ids': [sid], 'tags': [platform.lower(), 'needs-audit'],
    }


def candidates(sources):
    def body(sid):
        return (ROOT / sources[sid]['snapshot']).read_text()
    for title, url in re.findall(r'^\| \[([^\]]+)\]\((https://[^)]+)\)', body('dd-winners'), re.M):
        name = url.rstrip('/').removesuffix('.git').split('/')[-1]
        # Registry repository represents one candidate until year/track is resolved.
        yield record('dd-' + slug(name), title, url.removesuffix('.git'), 'DrivenData', 'dd-winners')
    for sid, year in [('vlsp-2023', 2023), ('vlsp-2025', 2025)]:
        parser = Links(); parser.feed(body(sid))
        seen = set()
        for href, title in parser.links:
            if f'vlsp{year}/eval/' not in href or not title or href in seen or href.rstrip('/').endswith('/registration'):
                continue
            seen.add(href)
            track = href.rstrip('/').split('/')[-1]
            yield record(f'vlsp-{year}-{slug(track)}', f'VLSP {year}: {title}',
                         urljoin('https://vlsp.org.vn', href), 'VLSP', sid, year, track, 'VLSP')
    # AIHUB: exclude classrooms, examples, generic event containers, legacy versions and VLSP duplicates.
    parser = Links(); parser.feed(body('aihub'))
    for href, text in parser.links:
        if not re.fullmatch(r'/competitions/\d+', href):
            continue
        title = text.split(' Organized by ')[0]
        lower = title.lower()
        if any(w in lower for w in ['vlsp', 'example', 'legacy', 'class 2026']) or not any(w in lower for w in ['2024', '2023', '2022', 'bkai']):
            continue
        if lower in ['viettel ai challenge', 'ucc ai quest 2023']:
            continue
        match = re.search(r'20\d{2}', title)
        year = int(match.group()) if match else None
        cid = 'aihub-' + href.split('/')[-1]
        r = record(cid, title, urljoin('https://aihub.ml', href), 'AIHUB.ML', 'aihub', year)
        r['tags'] += ['vietnam', 'vietnamese']
        yield r
    parser = Links(); parser.feed(body('dcase'))
    seen = set()
    for href, title in parser.links:
        if not href.startswith('/challenge2024/task-') or href.endswith('-results') or href in seen:
            continue
        seen.add(href)
        track = href.split('/task-')[-1]
        yield record('dcase-2024-' + track, 'DCASE 2024: ' + track.replace('-', ' '),
                     urljoin('https://dcase.community', href), 'DCASE', 'dcase', 2024, track, 'DCASE task organizers')
    parser = Links(); parser.feed(body('wmt'))
    seen = set()
    for href, title in parser.links:
        if not href.endswith('-task.html') or href.startswith('http'):
            continue
        url = urljoin('https://www2.statmt.org/wmt24/', href)
        if url in seen:
            continue
        seen.add(url)
        track = href.split('/')[-1].removesuffix('-task.html')
        yield record('wmt-2024-' + track, 'WMT 2024: ' + track.replace('-', ' '),
                     url, 'WMT', 'wmt', 2024, track, 'WMT task organizers')


def main():
    sources = {r['id']: r for r in json.loads((ROOT / 'catalog/sources/registry.json').read_text())}
    existing = {p.stem for folder in ['discovery', 'curated'] for p in (ROOT / 'catalog' / folder).glob('*.json')}
    count = 0
    for r in candidates(sources):
        if r['id'] in existing:
            continue
        target = ROOT / 'catalog/discovery' / (r['id'] + '.json')
        with target.open('x', encoding='utf-8') as out:
            out.write(json.dumps(r, ensure_ascii=False, indent=2) + '\n')
        existing.add(r['id']); count += 1
    print(f'Added {count} candidates; existing records preserved')


if __name__ == '__main__':
    main()
