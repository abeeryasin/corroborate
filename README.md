# Corroborate

Upload research papers, ask questions in plain English, get answers cited back to the specific paper and passage they came from — built with retrieval-augmented generation (RAG), not a chatbot wrapped around a folder of PDFs.

**Status:** core build complete (Steps 1–7 of 9) and independently evaluated — see [`docs/rag-evaluation.md`](docs/rag-evaluation.md). Deployment in progress.

## Why this exists

Reviewing literature means re-reading papers to re-find facts you already found once. Corroborate builds a queryable, cited memory over a chosen set of papers, scoped by workspace — ask a question, get an answer grounded only in what's actually in your uploaded papers, with the system saying "I don't know" rather than guessing when the answer isn't there.

## A real example

From the actual evaluation corpus (10 dengue-research papers):

> **Q: Which serotypes cause the most severe symptoms?**
> A: DENV3 was correlated with pleural effusion, poor capillary refill, and compensated shock... [with odds ratios cited directly from the paper's results, not its abstract]
>
> Sources: *Dengue severity by serotype and immune status in 19 years of pediatric clinical studies in Nicaragua* — Narvaez et al. (2025)

## Built with real evaluation, not just a demo

Most RAG demos show that a system *can* answer questions. [`docs/rag-evaluation.md`](docs/rag-evaluation.md) documents 10 real test questions run against the app, 6 that worked and 4 that failed — with each failure traced to a specific root cause: retrieval starvation on comparative questions, a paragraph fragmented mid-sentence by fixed-size chunking, and a corrupted PDF font encoding that silently degraded one paper's embeddings. Every claim in that document, in both the successes and the failures, was independently re-verified against the source PDFs before being written down.

[`docs/decisions.md`](docs/decisions.md) is a dated log of the real engineering tradeoffs made along the way and why — not a polished after-the-fact writeup.

## Stack

Python 3.12 · SQLite (raw `sqlite3`, no ORM — the SQL stays visible) · Chroma (vector search) · sentence-transformers (`all-MiniLM-L6-v2`, local embeddings) · Claude API (`claude-opus-4-8`) · Streamlit

## Architecture, honestly

This is currently one Python program, not a client/server split — Streamlit calls the ingestion, database, and RAG functions directly, in-process. A FastAPI layer was scaffolded in Step 1 but never built, and was removed rather than left as dead code once it was clear nothing yet needs that boundary. See [`docs/system-architecture.md`](docs/system-architecture.md) for the full frontend/backend boundary discussion and why that separation will eventually matter.

Papers are isolated by a `workspace` column, not full user authentication — a deliberate scope decision for a single-user app, reviewed and logged in [`docs/db-review-log.md`](docs/db-review-log.md), not an oversight.

## Setup

```
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then add your real ANTHROPIC_API_KEY
streamlit run frontend/streamlit_app.py
```

## Known limitations

- A real automated test suite exists (`tests/`, run via `pytest`) covering the chunking algorithm, the retrieval diversity fix, the database layer, and core Streamlit UI wiring — but it's the meaningful core, not full coverage. What it doesn't and can't check: whether the LLM's cleaned text output is actually *good* (a judgment call, not a pass/fail condition — that's what the RAG evaluation above is for).
- Storage is local-only (SQLite file + Chroma directory on disk) until deployment lands; see the deploy plan in `docs/decisions.md` for the persistent-storage tradeoff being made there.
- Fixed-size, non-overlapping chunking (documented, with real failure examples, in `docs/rag-evaluation.md`) — structure-aware chunking is a scoped v2 improvement, not an unknown gap.

## Documentation

- [`CLAUDE.md`](CLAUDE.md) — project overview, conventions, current roadmap position
- [`docs/decisions.md`](docs/decisions.md) — dated log of real decisions and the reasoning behind them
- [`docs/rag-evaluation.md`](docs/rag-evaluation.md) — 10 real test queries, verified successes and root-caused failures
- [`docs/system-architecture.md`](docs/system-architecture.md) — current frontend/backend boundary (or lack of one) and why
- [`docs/project-structure.md`](docs/project-structure.md) — what each folder contains and why (note: written early in the project and due for a refresh — some details, like `requirements.txt` being empty, are now stale)
