#!/usr/bin/env python3
"""Parse the Corpus Thomisticum index to map every work page to its URL.

Downloads iopera.html if not present, then outputs a JSON manifest of
{file, url, label} for all work pages.

Usage:
  python ct_parse_index.py            # downloads iopera.html, writes ct_manifest.json
"""
import re, json, html, os, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
INDEX_URL = 'https://www.corpusthomisticum.org/iopera.html'
INDEX_FILE = os.path.join(BASE, 'iopera.html')
MANIFEST_FILE = os.path.join(BASE, 'ct_manifest.json')

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'

# Nav pages to exclude (not work pages)
NAV = {'index.html', 'iopera.html', 'ealarcon.html', 'repedleo.html',
       'reoptedi.html', 'reopauth.html', 'tl.html', 'uabbrev.html',
       'ichartae.html', 'ibfonvit.html', 'ilcatope.html', 'ygoogle.html',
       'revincul.html', 'wintroen.html', 'wintrofr.html', 'wintronl.html',
       'wintrode.html', 'wintroes.html', 'wintrola.html', 'wintroit.html',
       'wintropl.html', 'wintropt.html', 'wintroeo.html', 'wintrosw.html'}


def download_index():
    if os.path.exists(INDEX_FILE) and os.path.getsize(INDEX_FILE) > 1000:
        return
    print(f"Downloading {INDEX_URL} ...")
    req = urllib.request.Request(INDEX_URL, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    with open(INDEX_FILE, 'wb') as f:
        f.write(data)
    print(f"Saved {INDEX_FILE} ({len(data)} bytes)")


def main():
    download_index()
    with open(INDEX_FILE, encoding='iso-8859-1') as f:
        content = f.read()

    pattern = re.compile(
        r'<A\s+HREF="https://www\.corpusthomisticum\.org/([a-z0-9]+\.html)"[^>]*>(.*?)</A>',
        re.IGNORECASE | re.DOTALL)

    pages = []
    for m in pattern.finditer(content):
        fname = m.group(1).lower()
        label = re.sub(r'<[^>]+>', '', m.group(2))
        label = html.unescape(label).strip()
        if fname in NAV:
            continue
        pages.append({'file': fname,
                      'url': f'https://www.corpusthomisticum.org/{fname}',
                      'label': label})

    # Dedupe by file
    seen = set()
    unique = []
    for p in pages:
        if p['file'] not in seen:
            seen.add(p['file'])
            unique.append(p)

    print(f"Total work pages: {len(unique)}")
    with open(MANIFEST_FILE, 'w', encoding='utf-8') as f:
        json.dump(unique, f, ensure_ascii=False, indent=2)
    print(f"Wrote {MANIFEST_FILE}")


if __name__ == '__main__':
    main()
