#!/usr/bin/env python3
"""Fetch an explicit list of public URLs. Never executes downloaded content."""
import argparse, concurrent.futures, datetime, hashlib, json, pathlib, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[1]
def fetch(item):
    url = item['url']
    if not url.startswith('https://'):
        raise ValueError('HTTPS required')
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    record = dict(item, retrieved_at=now)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'CompetitionResearchLab/0.1', 'Accept': 'application/json, text/plain, text/html'})
        with urllib.request.urlopen(req, timeout=35) as response:
            body = response.read(8_000_001)
            if len(body) > 8_000_000:
                raise ValueError('Snapshot exceeds 8 MB limit')
            record.update(final_url=response.url, http_status=response.status)
        digest = hashlib.sha256(body).hexdigest()
        path = ROOT / 'evidence' / 'snapshots' / (digest + '.txt')
        path.write_bytes(body)
        record.update(status='retrieved', sha256=digest, snapshot=str(path.relative_to(ROOT)), bytes=len(body))
    except Exception as exc:
        record.update(status='blocked', error=str(exc))
    return record
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=pathlib.Path)
    parser.add_argument('--output', required=True, type=pathlib.Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output log already exists; use a new dated log to preserve retrieval history')
    items = json.loads(args.manifest.read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        result = list(pool.map(fetch, items))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    for item in result:
        print(item['id'], item['status'], item.get('bytes', item.get('error')))
if __name__ == '__main__':
    main()
