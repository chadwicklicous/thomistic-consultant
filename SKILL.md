---
name: thomistic-consultant
description: "Answer Aquinas questions from the original Latin sources."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [thomas-aquinas, thomism, latin, philosophy, theology, vector-search, corpus-thomisticum]
    category: research
---

# Thomistic Consultant

Answer questions about St. Thomas Aquinas' philosophy and theology **from the original Latin sources**, grounded in the Corpus Thomisticum, with exact Leonine citations — not from the model's general recollection.

## When to Use

- User asks a question about Aquinas' philosophy or theology (metaphysics, epistemology, ethics, natural law, virtue, grace, the soul, God, etc.)
- User wants a passage located, a doctrine explained *secundum mentem Thomae*, or a citation verified
- User is writing/studying and needs the original Latin with a precise reference

## Setup (one-time — the agent runs this, not the user)

When the user first asks to use the Thomistic consultant, **the agent performs this setup autonomously**. The user should not have to run any commands, install any programs, or understand any of this. The user just talks to the agent in plain English.

The pipeline scripts are bundled in this skill's `scripts/` directory:
[`scripts/ct_parse_index.py`](scripts/ct_parse_index.py),
[`scripts/ct_download.py`](scripts/ct_download.py),
[`scripts/ct_extract.py`](scripts/ct_extract.py), and
[`scripts/ct_index.py`](scripts/ct_index.py).

Resolve the skill's directory (the directory containing this `SKILL.md`) and run
everything from there — no separate clone or download is needed.

1. **Install Python dependencies** (pinned version):
   ```bash
   pip install "chromadb==1.5.9"
   ```

2. **Install Ollama if it is not already present.** Check first:
   ```bash
   ollama --version
   ```
   If that fails, install it for the user's platform:
   - **Windows:** download and run the installer from https://ollama.com/download/OllamaSetup.exe
   - **macOS:** download and run https://ollama.com/download/Ollama-darwin.zip
   - **Linux:** `curl -fsSL https://ollama.com/install.sh | sh`
   Then start the Ollama service (on Windows/macOS the installer launches it; on
   Linux run `ollama serve` in the background).

3. **Pull the embedding model:**
   ```bash
   ollama pull nomic-embed-text
   ```

4. **Build the corpus and index.** This downloads ~656 pages and embeds 93,189
   paragraphs. It takes a few hours on CPU and is **resumable** — if it is
   interrupted, re-run `scripts/ct_index.py` and it continues from where it stopped.
   ```bash
   cd <skill-dir>/scripts
   python ct_parse_index.py     # map all work pages → URLs
   python ct_download.py        # download the corpus
   python ct_extract.py         # extract citation-tagged text
   python ct_index.py           # build the vector index
   ```

5. **Verify** the setup works:
   ```bash
   python ct_index.py --query "utrum Deus sit" --k 3
   ```
   If it returns passages with citations, the consultant is ready.

After setup, the user asks questions in natural language and the agent retrieves
the relevant Latin passages with citations.

## Query Workflow

### 1. Semantic retrieval

```bash
cd <skill-dir>/scripts
python ct_index.py --query "<the user's question, in Latin or English>" --k 5
```

This embeds the question and returns the top-k paragraphs with exact citations.
For a broader sweep, use `--k 10`.

### 2. Read the actual Latin

The query returns the passage text. Read it carefully. If you need the full
paragraph (the query truncates to 300 chars), grep the TSV:

```bash
grep -F "De veritate, q. 1 a. 2 co." <skill-dir>/scripts/thomistic/text/qdv01.tsv
```

### 3. Answer from the source

- Quote the **original Latin** passage.
- Give the **exact citation** (e.g. `ST I q. 2 a. 3 co.`).
- Explain the doctrine in the user's language, but anchor every claim in the quoted text.

## Citation format reference

| Form | Meaning |
|------|---------|
| `ST I q. 2 a. 3 co.` | Summa Theologiae, Pars I, q. 2, art. 3, corpus |
| `ST I-II q. 94 a. 2` | Prima Secundae, natural law |
| `De veritate, q. 1 a. 1 ad 2` | Disputed question, reply to obj. 2 |
| `De malo, q. 1 a. 1` | Disputed question on evil |
| `Contra Gentiles, lib. 1 cap. 13` | Summa contra Gentiles |
| `Super Sent., lib. 1 d. 3 q. 1 a. 1` | Sentences commentary |
| `Sententia Metaphysicae, lib. 4 l. 1` | Metaphysics commentary |
| `In Physic., lib. 1 l. 1` | Physics commentary |
| `Sentencia De anima, lib. 2 l. 1` | De anima commentary |

## Pitfalls

- **Don't answer from memory.** Always retrieve and quote the actual Latin. The whole point is citation-grounded answers.
- **The index build is resumable.** If `ct_index.py` dies partway (e.g. Ollama hiccup), just re-run it — it resumes from the last indexed count. The embed function retries and isolates bad paragraphs.
- **Ollama must be running** for embeddings (`ollama serve`). Model: `nomic-embed-text`.
- **Long paragraphs** are truncated to 6000 chars before embedding (nomic-embed context limit).
- **The 11 Gallica-restricted Leonina volumes** (t.22, 24, 26, 28, 40, 41, 42, 43, 45) are not publicly downloadable as PDFs, but their full text IS in the Corpus Thomisticum corpus — so the consultant covers them.

## Verification

1. Run a query and confirm it returns passages with valid citations.
2. Grep the TSV to confirm the full paragraph text matches the citation.
3. Answer a test question and confirm every claim is anchored in a quoted Latin passage.
