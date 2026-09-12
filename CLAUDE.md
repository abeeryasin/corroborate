# CLAUDE.md

## Project Overview

Corroborate — upload research papers, ask questions, get cited answers drawn from your own uploaded PDFs (retrieval-augmented generation). Portfolio + learning project — MVP scope only.

**Status: v1 complete and deployed, v2 bug fixes shipped 2026-08-25.** Live on Streamlit Community Cloud (production tracks `main`; staging tracks the `staging` branch — see `docs/staging-vs-production.md`). GitHub: `github.com/abeeryasin/corroborate`, public.

Stack: Python 3.12, SQLite for metadata (raw SQL, no ORM), Chroma for vectors, sentence-transformers for local embeddings, Claude API (`claude-opus-4-8` default) for generation, Streamlit frontend — Streamlit calls everything directly, in-process; no separate backend service exists (see `docs/system-architecture.md`).

## Context Window

Claude Code only holds a limited amount of text in memory per session — this shapes how the project is built:

1. **Ingestion happens in code, not in chat.** A full extracted paper could be tens of thousands of words — never pasted into a conversation to "have Claude read it." The ingestion pipeline reads and chunks it in Python; only small relevant chunks ever enter a prompt at query time. That's the actual mechanical reason RAG exists.
2. **This file is a compressed pointer, not a full history.** A fresh Claude Code session won't remember past conversations — it reads this file instead. Keep it short and update it after real changes.

## Key Commands

```
source .venv/bin/activate
pip install -r requirements.txt
streamlit run frontend/streamlit_app.py
```

## Working Style

- **Learning loop for every new step** (this project is the learning environment):
  1. Explain the concepts before writing any code — assume basic Python only.
  2. Write the code.
  3. Walk through it line by line.
  4. Point out common beginner mistakes tied to this specific code.
  5. Give a small, contained exercise — not "build the feature."
  6. Optionally, lightly quiz on the concept afterward, one question at a time, low-pressure.
- Raw SQL via `sqlite3`, no ORM — the SQL stays visible, not hidden behind an abstraction.
- Dependencies go into `requirements.txt` only when a step actually needs them, not front-loaded.
- Secrets live in `.env` (gitignored); `.env.example` holds placeholder keys only.
- Papers are scoped by a `workspace` column, not full user auth — see `docs/db-review-log.md`.
- **Staging workflow:** real code changes go `staging` branch → push → verify on the staging URL → merge to `main` → production. Docs-only edits go straight to `main` (no behavior risk). See `docs/decisions.md` (2026-08-23) for why this was adopted late rather than before the first deploy.

## Current Status

Roadmap (scaffold → DB → PDF ingestion → chunking/embeddings → Streamlit v1 → RAG Q&A → polish → deploy → eval) is complete — see `docs/decisions.md` for the dated log of each step's reasoning.

**v2, done 2026-08-25:** structure-aware ingestion (`app/ingestion/text_cleaner.py`), paragraph-aware chunking (`app/rag/chunking.py`), and a retrieval-diversity cap (`app/rag/vector_store.py`) — all three were real bugs documented in `docs/rag-evaluation.md`, all three now covered by `tests/`.

**Deferred, with reasons — don't re-suggest without new evidence:**
- Real persistent storage (hosted Postgres/Chroma Cloud, or a paid host with a mounted volume) — Streamlit Community Cloud's ephemeral storage was fine for a demo. Revisit if data needs to persist across days/weeks.
- Real uptime/SLA tracking — a `session_log` table was built then reverted; with one user who is also the operator, there's no one to make an availability promise to. SLA doc is conceptual only.
- Real escalation protocol (auto-pause + alert on error/cost spikes) — conceptual doc only, deferred to v3 if it turns out to be needed.
- LLM-as-judge answer-quality checking — scoped down to technical health monitoring only (errors, response time, "I don't know" rate); answer *correctness* can't be checked automatically without it.
- Soft delete / recycle bin — confirm-before-delete already covers the real risk (accidental irreversible deletion) without a schema migration.
- Study comparison, evidence tables, gap identification, decision tracking, agents, a standalone knowledge-graph exercise.

**v3 idea:** automatic literature search via PubMed/Semantic Scholar APIs.
