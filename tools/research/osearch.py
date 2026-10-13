#!/usr/bin/env python3
"""Ollama web_search / web_fetch helper.

API key: OLLAMA_API_KEY environment variable, or a `.ollama_key` file in the
repository root (gitignored). Never commit the key.

usage:
  osearch.py search OUTDIR "query1" "query2" ...   parallel searches, saves JSON, prints a compact summary
  osearch.py fetch OUTDIR url1 url2 ...            fetches pages, saves JSON, prints the start of each
env: N = results per query (default 6), SNIP = printed characters per item (default 350)
"""
import concurrent.futures as cf
import hashlib
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def load_key():
    key = os.environ.get('OLLAMA_API_KEY', '').strip()
    if not key and os.path.exists(os.path.join(ROOT, '.ollama_key')):
        key = open(os.path.join(ROOT, '.ollama_key')).read().strip()
    if not key:
        sys.exit('OLLAMA_API_KEY is not set and .ollama_key was not found')
    return key


KEY = load_key()


def post(endpoint, body, timeout=60):
    req = urllib.request.Request(
        f'https://ollama.com/api/{endpoint}', data=json.dumps(body).encode(),
        headers={'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json'})
    err = None
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.load(r)
        except Exception as e:
            err = e
    return {'error': str(err)}


def slug(s):
    return re.sub(r'[^a-zA-Z0-9]+', '_', s)[:60] + '_' + hashlib.md5(s.encode()).hexdigest()[:6]


def do_search(outdir, q, n):
    res = post('web_search', {'query': q, 'max_results': n})
    with open(os.path.join(outdir, 'S_' + slug(q) + '.json'), 'w') as f:
        json.dump({'query': q, **res}, f, ensure_ascii=False, indent=1)
    return q, res


def do_fetch(outdir, url):
    res = post('web_fetch', {'url': url}, timeout=90)
    with open(os.path.join(outdir, 'F_' + slug(url) + '.json'), 'w') as f:
        json.dump({'url': url, **res}, f, ensure_ascii=False, indent=1)
    return url, res


def main(argv):
    mode, outdir, *items = argv
    os.makedirs(outdir, exist_ok=True)
    snip = int(os.environ.get('SNIP', '350'))
    n = int(os.environ.get('N', '6'))
    with cf.ThreadPoolExecutor(8) as ex:
        if mode == 'search':
            for q, res in ex.map(lambda q: do_search(outdir, q, n), items):
                print(f'\n### Q: {q}')
                if 'error' in res:
                    print('  ERROR', res['error'])
                    continue
                for r in res.get('results') or []:
                    c = re.sub(r'\s+', ' ', r.get('content', ''))[:snip]
                    print(f"- {r.get('title', '')[:100]} | {r.get('url')}\n    {c}")
        elif mode == 'fetch':
            for u, res in ex.map(lambda u: do_fetch(outdir, u), items):
                print(f'\n### URL: {u}')
                if 'error' in res:
                    print('  ERROR', res['error'])
                    continue
                c = re.sub(r'\s+', ' ', res.get('content', ''))
                print(f"  title: {res.get('title')}  len={len(c)}\n  {c[:snip]}")
        else:
            sys.exit(__doc__)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    main(sys.argv[1:])
