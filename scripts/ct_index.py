#!/usr/bin/env python3
"""Build a ChromaDB vector index of the Thomistic corpus for semantic search.

Each paragraph (citation + Latin text) becomes a document. Embeddings come from
a configurable provider (default: Ollama's nomic-embed-text, 768-dim). The index
lives in thomistic/chroma/ and supports citation-grounded retrieval.

Configuration (environment variables, all optional):
  EMBED_PROVIDER   'ollama' (default) or 'openai'
  OLLAMA_URL       default http://localhost:11434
  EMBED_MODEL      default nomic-embed-text (ollama) or text-embedding-3-small (openai)
  OPENAI_API_KEY   required only if EMBED_PROVIDER=openai
  OPENAI_BASE_URL  optional, for OpenAI-compatible endpoints

Usage:
  python ct_index.py            # build/refresh the index
  python ct_index.py --query "utrum veritas sit in intellectu" --k 5
"""
import os, sys, json, time, urllib.request, urllib.error

BASE = os.path.dirname(os.path.abspath(__file__))
TXT = os.path.join(BASE, 'thomistic', 'text')
CHROMA_DIR = os.path.join(BASE, 'thomistic', 'chroma')
COLLECTION = 'thomistic_corpus'

PROVIDER = os.environ.get('EMBED_PROVIDER', 'ollama')
OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434')
EMBED_MODEL = os.environ.get('EMBED_MODEL',
    'nomic-embed-text' if PROVIDER == 'ollama' else 'text-embedding-3-small')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
OPENAI_BASE_URL = os.environ.get('OPENAI_BASE_URL', 'https://api.openai.com/v1')


def embed_ollama(texts):
    req = urllib.request.Request(
        f'{OLLAMA_URL}/api/embed',
        data=json.dumps({'model': EMBED_MODEL, 'input': texts}).encode(),
        headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.loads(r.read())
    return d['embeddings']


def embed_openai(texts):
    req = urllib.request.Request(
        f'{OPENAI_BASE_URL}/embeddings',
        data=json.dumps({'model': EMBED_MODEL, 'input': texts}).encode(),
        headers={'Content-Type': 'application/json',
                 'Authorization': f'Bearer {OPENAI_API_KEY}'})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.loads(r.read())
    return [item['embedding'] for item in d['data']]


def embed(texts):
    """Embed a list of texts. Robust: retries on transient errors; on a batch
    400, falls back to per-item embedding so one bad paragraph can't kill the run."""
    texts = [t[:6000] for t in texts]  # truncate very long paragraphs
    fn = embed_ollama if PROVIDER == 'ollama' else embed_openai
    for attempt in range(3):
        try:
            return fn(texts)
        except urllib.error.HTTPError as e:
            if e.code == 400 and len(texts) > 1:
                mid = len(texts) // 2
                return embed(texts[:mid]) + embed(texts[mid:])
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))


def load_paragraphs():
    paras = []
    for fname in sorted(os.listdir(TXT)):
        if not fname.endswith('.tsv'):
            continue
        with open(os.path.join(TXT, fname), encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n')
                if '\t' not in line:
                    continue
                cit, text = line.split('\t', 1)
                if text.strip():
                    paras.append((cit.strip(), text.strip()))
    return paras


def main():
    import chromadb
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    col = client.get_or_create_collection(
        name=COLLECTION,
        metadata={'hnsw:space': 'cosine'})

    paras = load_paragraphs()
    print(f"Loaded {len(paras)} paragraphs (provider={PROVIDER}, model={EMBED_MODEL})")

    existing = col.count()
    print(f"Already indexed: {existing}")

    BATCH = 32
    start = existing
    for i in range(start, len(paras), BATCH):
        batch = paras[i:i+BATCH]
        ids = [f"p{i+j}" for j in range(len(batch))]
        texts = [t for _, t in batch]
        cits = [c for c, _ in batch]
        vecs = embed(texts)
        col.add(ids=ids, embeddings=vecs,
                documents=texts,
                metadatas=[{'citation': c} for c in cits])
        if (i // BATCH) % 5 == 0:
            print(f"  indexed {i+len(batch)}/{len(paras)}")
    print(f"Index complete: {col.count()} vectors")


def query(q, k=5):
    import chromadb
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    col = client.get_collection(COLLECTION)
    vec = embed([q])[0]
    res = col.query(query_embeddings=[vec], n_results=k)
    return list(zip(res['metadatas'][0], res['documents'][0]))


if __name__ == '__main__':
    if '--query' in sys.argv:
        q = sys.argv[sys.argv.index('--query') + 1]
        k = int(sys.argv[sys.argv.index('--k') + 1]) if '--k' in sys.argv else 5
        for meta, doc in query(q, k):
            print(f"\n[{meta['citation']}]\n  {doc[:300]}")
    else:
        main()
