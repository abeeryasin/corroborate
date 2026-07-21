# Evidence Intelligence Platform

An AI-powered workspace for research literature: upload papers, ask questions, get answers cited back to the specific papers they came from — built with retrieval-augmented generation (RAG), not just a chatbot wrapped around PDFs.

**Status:** early development. See [`CLAUDE.md`](CLAUDE.md) for the current build step and roadmap.

## Why

Reviewing literature means re-reading papers to re-extract facts you already found once. This project builds a queryable, cited memory over a chosen set of papers — starting with a single core loop: upload → ask → get an answer grounded in your own collection, not a general-knowledge guess.

## Stack

Python 3.12 · FastAPI · SQLite · Chroma (vector search) · sentence-transformers (local embeddings) · Claude API · Streamlit

## Setup

```
source .venv/bin/activate
pip install -r requirements.txt
```

## Documentation

- [`CLAUDE.md`](CLAUDE.md) — project overview, conventions, current roadmap position
- [`docs/decisions.md`](docs/decisions.md) — dated log of real decisions and the reasoning behind them
- [`docs/course-alignment.md`](docs/course-alignment.md) — how this build maps to an external learning curriculum
- [`docs/project-structure.md`](docs/project-structure.md) — what each folder contains and why
- [`docs/timeline.md`](docs/timeline.md) — hour estimates per roadmap step
