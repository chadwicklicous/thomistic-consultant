# Thomistic Consultant

A citation-grounded consultant for the works of St. Thomas Aquinas. Builds a
semantic-search index over the complete **Corpus Thomisticum** (the critical
Latin text, ed. Enrique Alarcón, University of Navarra) and answers questions
**from the original Latin with exact Leonine citations** — not from a model's
general recollection.

## What it does

1. Downloads all 656 work pages of the Corpus Thomisticum (the full Latin text
   of Aquinas' complete works, including the works restricted on Gallica).
2. Extracts 93,189 paragraphs, each tagged with its exact citation
   (e.g. `De veritate, q. 1 a. 1 co.`).
3. Builds a ChromaDB vector index for semantic search.
4. Answers questions by retrieving the relevant Latin passages with citations.

## Two ways to use it

### For non-technical users (recommended): let your AI agent do the work

If you use **Hermes Agent** (or a similar AI agent), you don't need to run any
commands. Just:

1. Install the skill:
   ```bash
   hermes skills install chadwicklicous/thomistic-consultant
   ```
   (or copy this repo's `SKILL.md` + `scripts/` into your agent's skills folder)
2. Say: *"Set up the Thomistic consultant."*

Your agent reads the skill, installs the dependencies, downloads the corpus,
builds the index, and verifies it — all autonomously. Then you ask questions in
plain English and it answers from the original Latin with exact citations.

The skill is **self-contained**: the scripts are bundled in the skill's own
`scripts/` directory, so the agent runs everything from there — no separate
clone or download. The skill's **Setup** section is written as instructions
*for the agent to execute*, so the user never touches a terminal.

### For technical users: run it directly

The pipeline is standalone Python. See the Quick start below.

## Requirements

- **Python 3.9+** (stdlib only for the pipeline; `chromadb` for the index)
- **ChromaDB** — the vector database. Installed via `pip install chromadb` (in `requirements.txt`). No separate server needed; it runs embedded.
- **An embedding provider** — one of:
  - **Ollama** (free, local) with the `nomic-embed-text` model, or
  - **OpenAI** (or any OpenAI-compatible endpoint) with an embedding model
- **Hermes Agent** (optional) — to use the bundled `thomistic-consultant` skill
  that documents the query-and-answer workflow. The pipeline itself is
  standalone Python and works without Hermes.

### What is NOT required

- **Obsidian is not required.** The tool is pure Python + ChromaDB + an
  embedding provider. It does not download or depend on Obsidian, or any other
  note-taking app.
- **No API keys** are required if you use Ollama (free and local). An API key
  is only needed if you choose the OpenAI embedding provider.
- **No database server** — ChromaDB runs embedded, storing its index in a local
  directory.

## Quick start

```bash
# 1. Install dependencies
pip install chromadb

# 2. (Ollama users) pull the embedding model
ollama pull nomic-embed-text

# 3. Build the corpus (downloads ~656 pages, extracts text)
cd scripts
python ct_parse_index.py     # downloads the index, writes ct_manifest.json
python ct_download.py        # downloads all work pages to thomistic/raw/
python ct_extract.py         # extracts citation-tagged text to thomistic/text/

# 4. Build the vector index (embeds 93,189 paragraphs)
python ct_index.py

# 5. Query
python ct_index.py --query "utrum veritas sit in intellectu" --k 5
```

The index build takes a few hours on CPU (it embeds 93k paragraphs). It is
**resumable** — re-run `ct_index.py` and it continues from where it stopped.

## Configuration

All via environment variables (optional):

| Variable | Default | Purpose |
|----------|---------|---------|
| `EMBED_PROVIDER` | `ollama` | `ollama` or `openai` |
| `OLLAMA_URL` | `http://localhost:11434` | Ollama server |
| `EMBED_MODEL` | `nomic-embed-text` (ollama) / `text-embedding-3-small` (openai) | Embedding model |
| `OPENAI_API_KEY` | — | Required if `EMBED_PROVIDER=openai` |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | For OpenAI-compatible endpoints |

Example (OpenAI):

```bash
export EMBED_PROVIDER=openai
export OPENAI_API_KEY=sk-...
python ct_index.py
```

## Using with Hermes Agent

This repository **is** a Hermes skill — `SKILL.md` at the root, with the
pipeline scripts bundled in `scripts/`. Install it with:

```bash
hermes skills install chadwicklicous/thomistic-consultant
```

The skill's **Setup** section tells the agent to run the full pipeline
autonomously from the skill's own `scripts/` directory — the user just says
"set up the Thomistic consultant" and then asks questions in plain English. The
agent retrieves passages with `ct_index.py --query`, reads the full Latin, and
answers from the source with exact citations.

## How it works

```
corpusthomisticum.org
        │  ct_parse_index.py  (map 656 work pages → URLs)
        ▼
   iopera.html → ct_manifest.json
        │  ct_download.py  (fetch all pages)
        ▼
   thomistic/raw/*.html
        │  ct_extract.py  (parse <P TITLE="citation"> blocks)
        ▼
   thomistic/text/*.tsv   (93,189 citation-tagged paragraphs)
        │  ct_index.py  (embed + store in ChromaDB)
        ▼
   thomistic/chroma/  (vector index, collection "thomistic_corpus")
        │  ct_index.py --query "..."
        ▼
   top-k passages with exact Leonine citations
```

## Citation format

| Form | Meaning |
|------|---------|
| `ST I q. 2 a. 3 co.` | Summa Theologiae, Pars I, q. 2, art. 3, corpus |
| `De veritate, q. 1 a. 1 ad 2` | Disputed question, reply to objection 2 |
| `Contra Gentiles, lib. 1 cap. 13` | Summa contra Gentiles |
| `Super Sent., lib. 1 d. 3 q. 1 a. 1` | Sentences commentary |
| `Sententia Metaphysicae, lib. 4 l. 1` | Metaphysics commentary |

## License

MIT. The Corpus Thomisticum text is © Fundación Tomás de Aquino, used here for
research and study. See https://www.corpusthomisticum.org for the source.
