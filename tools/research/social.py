#!/usr/bin/env python3
"""Routes around sites that block normal search/fetch (tested 2026-10-13).

  social.py reddit-posts SUBREDDIT "title words" [AFTER=2024-01-01]   Arctic Shift post search (title match)
  social.py reddit-comments SUBREDDIT "body words" [AFTER]            Arctic Shift comment search (body match)
  social.py reddit-thread POST_ID                                     a post and its comments (POST_ID like 1x4vcqk)
  social.py yt-search "query"                                         YouTube search (videoId, title, channel, age, views)
  social.py yt-transcript VIDEO_ID                                    transcript via Ollama web_fetch (needs the API key)
  social.py x-post URL_OR_ID                                          one X/Twitter post via api.fxtwitter.com

What is blocked: reddit.com (403), pullpush (429), Redlib/Nitter mirrors (bot walls),
and Ollama fetch of reddit.com / x.com. X has no working search route, so collect
x.com status links from other pages and read them one by one with x-post.
Pass '' as SUBREDDIT to search all of Reddit (slower). Keep to about 1 request per second;
Arctic Shift answers "Timeout. Maybe slow down" when hammered.
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
ARCTIC = 'https://arctic-shift.photon-reddit.com/api'
HERE = os.path.dirname(os.path.abspath(__file__))


def get(url, timeout=45):
    err = None
    for i in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode('utf-8', 'replace')
        except Exception as e:
            err = e
            time.sleep(2 * (i + 1))
    return json.dumps({'error': str(err)})


def day(ts):
    return time.strftime('%Y-%m-%d', time.gmtime(ts)) if ts else '?'


def flat(s, n):
    return re.sub(r'\s+', ' ', s or '')[:n]


def reddit_search(kind, sub, words, after):
    key = 'title' if kind == 'posts' else 'body'
    params = {key: words, 'after': after, 'limit': 25, 'sort': 'desc'}
    if sub:
        params['subreddit'] = sub
    d = json.loads(get(f'{ARCTIC}/{kind}/search?' + urllib.parse.urlencode(params)))
    if d.get('error'):
        sys.exit(f"ERROR {d['error']}")
    for x in d.get('data') or []:
        if kind == 'posts':
            print(f"[{day(x.get('created_utc'))}] r/{x.get('subreddit')} id={x.get('id')} "
                  f"score={x.get('score')} cmts={x.get('num_comments')} :: {x.get('title')}\n"
                  f"    {flat(x.get('selftext'), 300)}  {x.get('url', '')}")
        else:
            print(f"[{day(x.get('created_utc'))}] r/{x.get('subreddit')} post={x.get('link_id', '')[3:]} "
                  f"score={x.get('score')} :: {flat(x.get('body'), 400)}")


def reddit_thread(pid):
    d = json.loads(get(f'{ARCTIC}/posts/ids?ids={pid}'))
    for x in d.get('data') or []:
        print(f"# [{day(x.get('created_utc'))}] r/{x.get('subreddit')} {x.get('title')}\n"
              f"{(x.get('selftext') or '')[:3000]}\n{x.get('url', '')}\n")
    d = json.loads(get(f'{ARCTIC}/comments/search?' + urllib.parse.urlencode({'link_id': pid, 'limit': 100})))
    for x in sorted(d.get('data') or [], key=lambda c: -(c.get('score') or 0)):
        print(f"- ({x.get('score')}) {flat(x.get('body'), 600)}")


def yt_search(query):
    html = get('https://www.youtube.com/results?' + urllib.parse.urlencode({'search_query': query}))
    m = re.search(r'var ytInitialData = (\{.*?\});</script>', html)
    if not m:
        sys.exit('ERROR: no ytInitialData in the page')

    def walk(o):
        if isinstance(o, dict):
            if 'videoRenderer' in o:
                yield o['videoRenderer']
            for v in o.values():
                yield from walk(v)
        elif isinstance(o, list):
            for v in o:
                yield from walk(v)

    def text(r, k):
        f = r.get(k) or {}
        return ''.join(x.get('text', '') for x in f.get('runs', [])) or f.get('simpleText', '')

    for v in list(walk(json.loads(m.group(1))))[:20]:
        print(f"{v.get('videoId')} | {text(v, 'title')} | {text(v, 'ownerText')} | "
              f"{text(v, 'publishedTimeText')} | {text(v, 'viewCountText')} | {text(v, 'lengthText')}")


def yt_transcript(video_id):
    env = dict(os.environ)
    env.setdefault('SNIP', '12000')
    subprocess.run([sys.executable, '-I', os.path.join(HERE, 'osearch.py'), 'fetch',
                    os.path.join('research_raw', 'youtube'), f'https://www.youtube.com/watch?v={video_id}'],
                   env=env, check=False)


def x_post(url_or_id):
    m = re.search(r'(\d+)\D*$', url_or_id)
    if not m:
        sys.exit('ERROR: no post id found')
    d = json.loads(get(f'https://api.fxtwitter.com/status/{m.group(1)}'))
    tw = d.get('tweet') or {}
    if not tw:
        sys.exit(f'ERROR {d}')
    print(f"@{tw.get('author', {}).get('screen_name')} {tw.get('created_at')} "
          f"likes={tw.get('likes')} :: {tw.get('text')}")
    for media in (tw.get('media') or {}).get('all', []):
        print('  media:', media.get('url'))


def main(argv):
    if not argv:
        sys.exit(__doc__)
    cmd, *a = argv
    if cmd in ('reddit-posts', 'reddit-comments'):
        reddit_search('posts' if cmd == 'reddit-posts' else 'comments', a[0], a[1],
                      a[2] if len(a) > 2 else '2024-01-01')
    elif cmd == 'reddit-thread':
        reddit_thread(a[0])
    elif cmd == 'yt-search':
        yt_search(a[0])
    elif cmd == 'yt-transcript':
        yt_transcript(a[0])
    elif cmd == 'x-post':
        x_post(a[0])
    else:
        sys.exit(__doc__)


if __name__ == '__main__':
    main(sys.argv[1:])
