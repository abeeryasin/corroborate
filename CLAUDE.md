# CLAUDE.md

## Project Overview

Corroborate — upload research papers, ask questions, get cited answers drawn from your own uploaded PDFs (retrieval-augmented generation). Portfolio + learning project — MVP scope only.

**Status as of 2026-08-23: v1 complete and deployed.** Live on Streamlit Community Cloud (production tracks `main`; a separate staging app tracks the `staging` branch — exact URLs live in the user's Streamlit Cloud dashboard, not recorded here to avoid a stale/guessed link). GitHub: `github.com/abeeryasin/corroborate`, public.

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
- Papers are scoped by a `workspace` column (not full user auth) — see `docs/db-review-log.md`.
- Phases 1–3 of the course (mental models, mindset shift, memory architecture) were already completed in a prior project, before this repo existed — no dedicated artifacts needed for those phases here. Instead, proactively call it out in the moment whenever current work is genuinely applying a Phase 1–3 concept (closing the loop, context window awareness, producer vs. consumer mindset, the project's own memory architecture, etc.) — even without a file to point to, so the user stays aware they're still practicing it, not just that it was checked off once elsewhere.
- **Staging workflow (adopted 2026-08-23, SLO 5.14):** two separate Streamlit Community Cloud apps exist — production (tracks `main`) and staging (tracks the `staging` branch, its own separate URL). Real code changes that could affect app behavior go: commit to `staging` → push → verify on the staging URL → merge `staging` into `main` → push `main` → live on production. Docs-only edits (no behavior change) go straight to `main` — using staging for everything indiscriminately would be following the letter of the practice without the reasoning behind it. This was flagged late — should have been raised before the first deploy, not after several pushes (including one real incident) had already gone straight to production; adopted going forward rather than left as a retrospective-only lesson.

## Current Status

**Roadmap complete — all 9 steps done as of 2026-08-23. No step is "current" anymore.** For context on what each step involved:

1. Scaffold — done
2. Metadata DB (SQLite) — done
3. PDF ingestion — done
4. Chunking + embeddings — done
5. Streamlit v1 — done
6. RAG Q&A (the centerpiece) — done
7. Polish — done (workspace picker, delete-with-confirm, question history, `app/api/` cleanup, README overhaul)
8. Deploy — done 2026-08-23 (GitHub + Streamlit Community Cloud + staging workflow + all 5 deploy-adjacent SLO docs: `deployment-rationale.md`, `safety-monitoring.md`, `escalation-protocol.md`, `sla-definition.md`, `staging-vs-production.md`, `observability.md`)
9. Light eval — done 2026-08-19 (out of order, ahead of Deploy) — see `docs/rag-evaluation.md`

**v2 bug fixes — done 2026-08-25.** Both real, documented failures from `docs/rag-evaluation.md` are fixed and verified: structure-aware ingestion (`app/ingestion/text_cleaner.py` — Claude rewrites messy PDF text into clean Markdown before chunking) and paragraph-aware chunking (`app/rag/chunking.py` — splits on real paragraph boundaries instead of a blind character count, never orphaning a section heading from its content). A retrieval-diversity fix was added alongside them (`app/rag/vector_store.py` — caps results per paper so one paper can't crowd out a different relevant one). A real automated test suite now exists (`tests/`, run via `pytest`) covering all three, plus the database layer and core Streamlit UI wiring.

**Course/curriculum tracking has been fully separated out of this repo (2026-08-25).** The interview-prep pass across the external course's SLOs happened, then was deliberately removed from this public repo along with its tracking document — that material now lives in the user's own private notes, not here. Remaining course material not yet covered is deferred to a separate future project, not tracked in Corroborate anymore.

**v2, not now:** study comparison, evidence tables, gap identification, decision tracking, agents, a standalone knowledge-graph exercise. Also: a real recycle bin (soft delete — `deleted_at` column, restore via re-running the ingestion pipeline since Chroma embeddings would need re-creating) — deferred 2026-08-20 in favor of the cheaper confirm-before-delete step already shipped, which covers the main risk (accidental irreversible deletion) without a schema migration. Also: real uptime/SLA tracking (a `session_log` table was actually built and then deliberately reverted 2026-08-22 — the data could only ever prove uptime, never downtime, and with a single user who *is* the operator, there's no one to make an availability promise to that they don't already know firsthand) — SLA doc written as a conceptual doc for v1 instead, same reasoning as escalation protocol. Also: a real escalation protocol (error-rate/cost/"I don't know"-spike thresholds that actually pause the app and alert a human operator, not just the existing per-question "I don't know" stop) — written as a conceptual doc for v1 instead, deferred to v3 if it turns out to be needed. Also: LLM-as-judge answer-quality checking (a second AI call evaluates whether the first one's answer is well-grounded) — scoped down for v1 to technical/system health monitoring only (errors, response time, "I don't know" rate), since answer *correctness* can't be checked automatically without this. Also: real persistent storage for the deployed app — migrate off local SQLite/Chroma files to an external hosted DB (e.g. Postgres + Chroma Cloud), or move to a paid host with a mounted persistent volume (Railway Hobby, ~$5/mo, smallest real code change) — deferred 2026-08-20 in favor of accepting ephemeral storage on Streamlit Community Cloud for the deploy. Trigger to revisit: if this stops being a demo/portfolio app and becomes something the user (or their brother, reviewing informally) actually wants to keep using with data persisting across days/weeks.
**v3 idea:** automatic literature search via PubMed/Semantic Scholar APIs (see project memory for constraints).
