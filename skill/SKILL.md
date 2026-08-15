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

## The Corpus (already built)

- **Text corpus:** `C:\Users\philo\deep-research\thomistic\text\` — 656 TSV files, 93,189 paragraphs, each `CITATION\tTEXT`
- **Vector index:** `C:\Users\philo\deep-research\thomistic\chroma\` — ChromaDB collection `thomistic_corpus`, nomic-embed-text (768-dim)
- **Critical edition PDFs:** `C:\Users\philo\Library\Philosophy\Aquinas\EditioLeonina\` (22 vols) — for apparatus cross-reference
- **Obsidian index:** `What Animates Man/Thomistic Corpus/Index.md`

## Query Workflow

### 1. Semantic retrieval

```bash
cd /c/Users/philo/deep-research
python ct_index.py --query "<your question in Latin or English>" --k 5
```

This embeds the question and returns the top-k paragraphs with exact citations. For a broader sweep, use `--k 10`.

### 2. Read the actual Latin

The query returns the passage text. Read it carefully. If you need the full paragraph (the query truncates to 300 chars), grep the TSV:

```bash
grep -F "De veritate, q. 1 a. 2 co." /c/Users/philo/deep-research/thomistic/text/qdv01.tsv
```

### 3. Answer from the source

- Quote the **original Latin** passage.
- Give the **exact citation** (e.g. `ST I q. 2 a. 3 co.`).
- Explain the doctrine in the user's language, but anchor every claim in the quoted text.
- If the user wants the critical apparatus, point to the corresponding Leonina PDF volume.

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
- **Windows paths:** use `C:\Users\philo\...` or `/c/Users/philo/...` in bash, not `$HOME`.
- **The 11 Gallica-restricted Leonina volumes** (t.22, 24, 26, 28, 40, 41, 42, 43, 45) are NOT in the PDF library, but their full text IS in the Corpus Thomisticum corpus — so the consultant covers them.

## Verification

1. Run a query and confirm it returns passages with valid citations.
2. Grep the TSV to confirm the full paragraph text matches the citation.
3. Answer a test question and confirm every claim is anchored in a quoted Latin passage.

## Related

- `obsidian` — the vault where the corpus index lives
- `research-library-organization` — the library structure (Leonina PDFs)
