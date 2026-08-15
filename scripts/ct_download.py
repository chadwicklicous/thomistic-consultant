#!/usr/bin/env python3
"""Download all Corpus Thomisticum work pages to thomistic/raw/.

Resumable: skips files already downloaded. Uses urllib (stdlib only, no
requests dependency). Requires ct_manifest.json (run ct_parse_index.py first).

Usage:
  python ct_download.py
"""
import json, os, time, urllib.request, urllib.error

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, 'thomistic', 'raw')
os.makedirs(RAW, exist_ok=True)

with open(os.path.join(BASE, 'ct_manifest.json'), encoding='utf-8') as f:
    pages = json.load(f)

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'


def fetch(url, retries=4):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(2 * (attempt + 1))


def main():
    ok, fail = 0, 0
    for i, p in enumerate(pages):
        fname = p['file']
        out = os.path.join(RAW, fname)
        if os.path.exists(out) and os.path.getsize(out) > 1000:
            ok += 1
            continue
        try:
            data = fetch(p['url'])
            with open(out, 'wb') as f:
                f.write(data)
            ok += 1
        except Exception as e:
            fail += 1
            print(f"FAIL {fname}: {e}")
        if (i + 1) % 50 == 0:
            print(f"  ... {i+1}/{len(pages)} (ok={ok}, fail={fail})")
        time.sleep(0.15)  # be polite to the server

    print(f"DONE: ok={ok}, fail={fail}, total={len(pages)}")


if __name__ == '__main__':
    main()
