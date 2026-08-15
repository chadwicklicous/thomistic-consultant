# Thomistic Consultant — What It Is and What It Offers

## What it is

**Thomistic Consultant** is a research tool that turns the complete Latin works of St. Thomas Aquinas into a searchable, citation-grounded knowledge base. It downloads the full **Corpus Thomisticum** — the critical edition of Aquinas' *Opera omnia* maintained by the University of Navarra — extracts every paragraph with its exact scholarly citation, and builds a semantic-search index so you can ask questions in plain language and retrieve the *actual Latin passages* that answer them, each with its precise reference.

It is not a chatbot that paraphrases Aquinas from memory. It is a **retrieval engine** that grounds every answer in the original text, with verifiable citations you can check against the critical edition.

## What it offers

### 1. The complete corpus, locally

- **656 work pages** — the full *Opera omnia*: the *Summa Theologiae*, *Summa contra Gentiles*, the *Scriptum super Sententiis*, all the disputed questions (*De veritate*, *De malo*, *De potentia*, *De anima*, *De virtutibus*), the biblical commentaries, the Aristotelian commentaries, the *Catena aurea*, the Quodlibets, and the opuscula.
- **93,189 paragraphs**, each tagged with its exact Leonine citation (e.g. `ST I q. 2 a. 3 co.`, `De veritate q. 1 a. 1 ad 2`).
- Includes works that are **restricted on Gallica/BnF** (pulled from public access in 2024) — the full text is still available here.

### 2. Citation-grounded retrieval

Ask a question in Latin or English, and the tool returns the top passages with their exact citations:

```
$ python ct_index.py --query "utrum veritas sit in intellectu" --k 5

[De veritate, q. 1 a. 2 co.]
  Solutio. Dicendum, quod non oportet in illis quae dicuntur per prius...
```

Every answer can be traced to a specific passage in the critical edition. No hallucinated citations, no vague paraphrase.

### 3. Semantic search over the original Latin

The index uses **vector embeddings** (nomic-embed-text via Ollama, or any OpenAI-compatible embedding model), so you can search by *meaning*, not just by keyword. Ask about a concept — "the five ways," "synderesis," "the agent intellect" — and retrieve the relevant passages even when the exact wording differs.

### 4. A documented workflow for AI agents

The bundled **Hermes Agent skill** (`thomistic-consultant`) documents the full query-and-answer workflow: retrieve passages, read the full Latin, and answer *from the source* with exact citations. This makes the tool usable not just by humans but by AI assistants that need to ground their answers in primary sources.

### 5. Portable and self-contained

- **No API keys required** (Ollama is free and local; OpenAI is optional).
- **Resumable build** — the index can be built incrementally and interrupted safely.
- **~90 KB of code** — the corpus is downloaded at build time, not distributed, so the repository stays tiny and the licensing stays clean.

## Who it's for

- **Scholars and students** of Aquinas, Thomism, medieval philosophy, and theology who want to locate passages and verify citations quickly.
- **Researchers** building citation-grounded AI systems over primary sources.
- **Anyone** who wants to ask questions about Aquinas and get answers anchored in the original Latin rather than a model's recollection.

## The philosophy behind it

The tool embodies a specific view of what AI is good for: **retrieval, systematization, and consistency-checking** — not judgment. It retrieves the texts with superhuman recall, but the *judgment* of what the texts mean, and whether they are true, remains with the human reader. It is a **prosthetic for reasoning**, not a replacement for the intellect.

For a fuller treatment of this view, see the companion essay *De Cognitione Artificiali* (in the author's research corpus).
