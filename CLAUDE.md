# CLAUDE.md

## Project Overview

Corroborate — upload research papers, ask questions, get cited answers drawn from your own uploaded PDFs (retrieval-augmented generation). Portfolio + learning project — MVP scope only. See `docs/course-alignment.md` for how this maps to an external learning curriculum.

Stack: Python 3.12, SQLite for metadata (raw SQL, no ORM), Chroma for vectors, sentence-transformers for local embeddings, Claude API (`claude-opus-4-8` default) for generation, Streamlit frontend — Streamlit calls everything directly, in-process; no separate backend service exists (a FastAPI layer was scaffolded in Step 1, never built, and removed 2026-08-20 since nothing needs that boundary yet — see docs/system-architecture.md).

## Context Window

Claude (and Claude Code) only holds a limited amount of text in memory per session — this shapes how we build and interact with this project, concretely:

1. **Ingestion happens in code, not in chat.** A full extracted paper could be tens of thousands of words. We never paste raw paper text into a conversation to "have Claude read it" — the ingestion pipeline (Step 3–4) reads and chunks it in Python, and only small relevant chunks ever enter a prompt at query time. That's the actual mechanical reason RAG exists: it's a workaround for the context window limit, not just a buzzword.
2. **This file is a compressed pointer, not a full history.** A fresh Claude Code session (or a fresh me, next week) won't remember this conversation. Instead of re-deriving the project's state by reading every past chat, it reads this file. That's why we keep it short and update it after real changes — it has to carry the essential state in a fraction of the space a full history would take.

## Key Commands

```
source .venv/bin/activate
pip install -r requirements.txt
streamlit run frontend/streamlit_app.py
```

## Preferences

- **Learning loop for every new step** (this project IS the learning environment — there are no separate lectures to learn from first). Reverted 2026-08-19 to this version after trying a stricter "implement it yourself" loop that assumed more baseline fluency than week-1-of-Python actually has — revisit the stricter version later once fundamentals are solid, not before:
  1. Explain the concepts needed for this step before writing any code — assume basic Python only, explain what tool/pattern we're using, why, and how it fits the architecture.
  2. Write the code.
  3. Walk through it line by line.
  4. Point out common beginner mistakes tied to this specific code.
  5. Give a small, contained exercise — not "build the feature," something scoped enough to attempt from what was just explained.
  6. Optionally, lightly quiz on the concept afterward — one question at a time, don't give the answer unless stuck after trying. Keep this low-pressure, not a mandatory gate.
- Raw SQL via `sqlite3`, no ORM — the SQL should stay visible, not hidden behind an abstraction.
- Dependencies go into `requirements.txt` only when a step actually needs them, not front-loaded.
- Secrets live in `.env` (gitignored); `.env.example` holds placeholder keys only.
- Papers are scoped by a `workspace` column (not full user auth) — see docs/course-alignment.md.
- When a concept being taught maps to a specific SLO in docs/course-alignment.md, name the SLO number and description explicitly, in the moment — don't just track it silently after the fact. The user genuinely wants to know what course material they've learned and where, not just have it checked off in a document they don't see.
- Phases 1–3 of the course (mental models, mindset shift, memory architecture) were already completed in a prior project, before this repo existed — no dedicated artifacts needed for those phases here. Instead, proactively call it out in the moment whenever current work is genuinely applying a Phase 1–3 concept (closing the loop, context window awareness, producer vs. consumer mindset, the project's own memory architecture, etc.) — even without a file to point to, so the user stays aware they're still practicing it, not just that it was checked off once elsewhere.

## Current Status

Roadmap — build one step at a time:

1. Scaffold
2. Metadata DB (SQLite)
3. PDF ingestion
4. Chunking + embeddings
5. Streamlit v1
6. RAG Q&A (the centerpiece)
7. Polish ← current
8. Deploy — includes GitHub setup first (confirmed 2026-08-20: no GitHub account exists yet, and this repo has no remote configured — `git remote -v` is empty. Needed before any deploy host can be used, since e.g. Streamlit Community Cloud deploys from a GitHub repo, not local files. Also one of the project's original 5 success criteria ("polished GitHub repo"), not just deploy plumbing.)
9. Light eval — done (2026-08-19, out of order ahead of Deploy) — see `docs/rag-evaluation.md`

**v2, not now:** study comparison, evidence tables, gap identification, decision tracking, agents, a standalone knowledge-graph exercise. Also: structure-aware ingestion (PDF → clean Markdown before chunking, e.g. via an LLM, instead of raw `pypdf` text) + section/paragraph-aware chunking instead of fixed-1000-character splitting — justified by two real failures found during the Step 7 eval (`docs/rag-evaluation.md`): a mid-sentence chunk split, and page headers/footers bleeding into body text mid-paragraph. Also: a real recycle bin (soft delete — `deleted_at` column, restore via re-running the ingestion pipeline since Chroma embeddings would need re-creating) — deferred 2026-08-20 in favor of the cheaper confirm-before-delete step already shipped, which covers the main risk (accidental irreversible deletion) without a schema migration. Also: LLM-as-judge answer-quality checking (a second AI call evaluates whether the first one's answer is well-grounded) — for SLO 5.5/5.19, scoped down for v1 to technical/system health monitoring only (errors, response time, "I don't know" rate), since answer *correctness* can't be checked automatically without this. Also: real persistent storage for the deployed app — migrate off local SQLite/Chroma files to an external hosted DB (e.g. Postgres + Chroma Cloud), or move to a paid host with a mounted persistent volume (Railway Hobby, ~$5/mo, smallest real code change) — deferred 2026-08-20 in favor of accepting ephemeral storage on Streamlit Community Cloud for the deploy. Trigger to revisit: if this stops being a demo/portfolio app and becomes something the user (or their brother, reviewing informally) actually wants to keep using with data persisting across days/weeks.
**v3 idea:** automatic literature search via PubMed/Semantic Scholar APIs (see project memory for constraints).
