# CLAUDE.md

## Project Overview

Evidence Intelligence Platform — upload research papers, ask questions, get cited answers drawn from your own uploaded PDFs (retrieval-augmented generation). Portfolio + learning project — MVP scope only. See `docs/course-alignment.md` for how this maps to an external learning curriculum.

Stack: Python 3.12 + FastAPI backend, SQLite for metadata (raw SQL, no ORM), Chroma for vectors, sentence-transformers for local embeddings, Claude API (`claude-opus-4-8` default) for generation, Streamlit frontend.

## Context Window

Claude (and Claude Code) only holds a limited amount of text in memory per session — this shapes how we build and interact with this project, concretely:

1. **Ingestion happens in code, not in chat.** A full extracted paper could be tens of thousands of words. We never paste raw paper text into a conversation to "have Claude read it" — the ingestion pipeline (Step 3–4) reads and chunks it in Python, and only small relevant chunks ever enter a prompt at query time. That's the actual mechanical reason RAG exists: it's a workaround for the context window limit, not just a buzzword.
2. **This file is a compressed pointer, not a full history.** A fresh Claude Code session (or a fresh me, next week) won't remember this conversation. Instead of re-deriving the project's state by reading every past chat, it reads this file. That's why we keep it short and update it after real changes — it has to carry the essential state in a fraction of the space a full history would take.

## Key Commands

```
source .venv/bin/activate
pip install -r requirements.txt
```

## Preferences

- Explain a new concept before writing code that uses it — this is a learning project for someone new to Python/SQL.
- Raw SQL via `sqlite3`, no ORM — the SQL should stay visible, not hidden behind an abstraction.
- Dependencies go into `requirements.txt` only when a step actually needs them, not front-loaded.
- Secrets live in `.env` (gitignored); `.env.example` holds placeholder keys only.
- Papers are scoped by a `workspace` column (not full user auth) — see docs/course-alignment.md.
- When a concept being taught maps to a specific SLO in docs/course-alignment.md, name the SLO number and description explicitly, in the moment — don't just track it silently after the fact. The user genuinely wants to know what course material they've learned and where, not just have it checked off in a document they don't see.

## Current Status

Roadmap — build one step at a time:

1. Scaffold
2. Metadata DB (SQLite)
3. PDF ingestion
4. Chunking + embeddings ← current
5. Streamlit v1
6. RAG Q&A (the centerpiece)
7. Polish
8. Deploy
9. Light eval

**v2, not now:** study comparison, evidence tables, gap identification, decision tracking, agents, a standalone knowledge-graph exercise.
**v3 idea:** automatic literature search via PubMed/Semantic Scholar APIs (see project memory for constraints).
