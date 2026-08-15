#!/usr/bin/env python3
"""Extract clean Latin text with citations from Corpus Thomisticum HTML pages.

Each paragraph in the source carries a TITLE attribute with the exact citation,
e.g. TITLE="De veritate, q. 1 a. 1 co."  We extract each such paragraph into a
line:  [CITATION]\tTEXT

Output: thomistic/text/<file>.tsv  (one paragraph per line, tab-separated)

Usage:
  python ct_extract.py
"""
import os, re, html

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, 'thomistic', 'raw')
TXT = os.path.join(BASE, 'thomistic', 'text')
os.makedirs(TXT, exist_ok=True)

# A paragraph block: <P TITLE="CITATION"> ... </P>  OR  <DIV CLASS="cuatro" TITLE="CITATION"> ... </DIV>
P_PAT = re.compile(
    r'<(?:P|DIV)\b[^>]*TITLE="([^"]+)"[^>]*>(.*?)</(?:P|DIV)>',
    re.IGNORECASE | re.DOTALL)


def clean_text(s, citation=None):
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\[\d+\]\s*', '', s)
    s = html.unescape(s)
    s = re.sub(r'\s+', ' ', s).strip()
    if citation:
        s = s.replace(citation, '', 1).strip()
    return s


def extract(fname):
    path = os.path.join(RAW, fname)
    if not os.path.exists(path):
        return None
    with open(path, encoding='iso-8859-1', errors='replace') as f:
        content = f.read()
    paras = []
    for m in P_PAT.finditer(content):
        citation = m.group(1).strip()
        text = clean_text(m.group(2), citation)
        if not text:
            continue
        paras.append((citation, text))
    return paras


def main():
    files = sorted(f for f in os.listdir(RAW) if f.endswith('.html'))
    total_paras = 0
    for fname in files:
        paras = extract(fname)
        if not paras:
            continue
        out = os.path.join(TXT, fname.replace('.html', '.tsv'))
        with open(out, 'w', encoding='utf-8') as f:
            for cit, text in paras:
                f.write(f"{cit}\t{text}\n")
        total_paras += len(paras)
    print(f"Extracted {total_paras} paragraphs from {len(files)} pages")


if __name__ == '__main__':
    main()
