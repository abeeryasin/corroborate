# Project Structure

What actually exists right now, and why — refreshed 2026-08-25 after it drifted stale since 2026-08-20 (it still said "no automated test suite yet" and was missing every doc written since then).

```
Research/
├── .venv/                    Private Python environment (gitignored — not in the repo)
├── .gitignore
├── CLAUDE.md                 Project handbook — read by every future coding session
├── README.md                 Human-facing intro
├── requirements.txt          7 real dependencies, added one per roadmap step as needed
│                             (pypdf, sentence-transformers, chromadb, streamlit,
│                             anthropic, python-dotenv, pytest)
│
├── app/                      The actual application logic
│   ├── __init__.py             (marks app/ as an importable Python package)
│   ├── db/                      SQLite schema + raw SQL, no ORM (schema.py, queries.py)
│   ├── ingestion/                PDF → text → clean Markdown → auto-detected metadata
│   │                             (pdf_extractor.py, text_cleaner.py, metadata_extractor.py)
│   └── rag/                      Chunking, embeddings, Chroma vector store, and Claude
│                                 generation — the centerpiece
│                                 (chunking.py, vector_store.py, generation.py)
│
├── frontend/
│   └── streamlit_app.py       The entire UI — upload, workspace picker, delete, ask a question
│
├── scripts/
│   └── ingest_papers.py       Bulk-ingest a folder of PDFs into a workspace from the
│                             command line — same pipeline the UI uses, for many papers at once
│
├── .claude/skills/
│   └── launch-app/            Reusable skill capturing exact launch commands and real
│                             gotchas hit while browser-testing this app (cold-start timing,
│                             Streamlit widget quirks) — not a checkbox artifact
│
├── data/                       Generated at runtime, gitignored (not in the repo)
│   ├── papers.db                 SQLite database
│   ├── chroma/                   Chroma's persistent vector store
│   └── uploads/                  The actual PDF files papers were ingested from
│
├── tests/                      A real automated suite, run via `pytest` — chunking algorithm,
│                             retrieval diversity, database layer, core Streamlit UI wiring
│                             (test_chunking.py, test_vector_store.py, test_db_queries.py,
│                             test_streamlit_app.py, test_text_cleaner.py). Doesn't and can't
│                             cover LLM output *quality* — that's docs/rag-evaluation.md's job.
│
└── docs/
    ├── decisions.md               The "why" log — every real decision, dated
    ├── rag-evaluation.md          10 real test queries, verified successes and root-caused failures
    ├── system-architecture.md     The frontend/backend boundary — what exists, what doesn't, why
    ├── project-explainer.md       Plain-language architecture walkthrough, beginner-level
    ├── db-vocabulary.md           Database terms in plain language, tied to the real schema
    ├── data-modeling.md           Relational vs. flat data, applied to this project
    ├── db-review-log.md           Dated log of critically evaluating this project's own DB decisions
    ├── api-test.md                What an API actually is, using this project's real Claude call
    ├── env-security.md            Why secrets live in .env and never in code
    ├── deployment-rationale.md    Why Streamlit Community Cloud, researched against real alternatives
    ├── safety-monitoring.md       The real System Health dashboard — what it tracks and why
    ├── escalation-protocol.md     What's built today vs. what a real escalation system would need
    ├── sla-definition.md          An honest uptime promise for a solo demo app, not fabricated data
    ├── staging-vs-production.md   The real staging workflow, adopted after a real incident
    ├── observability.md           Real cost tracking computed from actual API usage
    ├── project-structure.md       This file
    └── timeline.md                Hour estimates per roadmap step
```

## Notes

- **The folder structure still *is* the roadmap, laid out physically** — same principle as when this doc was first written, just with the folders actually filled in now instead of being placeholders.
- **`app/api/` was scaffolded in Step 1, never built, and removed 2026-08-20** rather than left as dead code — see the README and `docs/system-architecture.md` for the reasoning (no second consumer of a backend API exists yet, so the boundary has no payoff yet). If that changes, the folder comes back with real code in it, not as a placeholder.
- **No `app/main.py` exists, and there's no plan to add one** unless a real FastAPI boundary becomes necessary — Streamlit itself is the entrypoint (`frontend/streamlit_app.py`).
- **`app/ingestion/text_cleaner.py` (added 2026-08-25)** rewrites messy PDF-extracted text into clean Markdown, via Claude, before chunking ever runs — real paragraph structure doesn't exist in raw `pypdf` output, so chunking couldn't be made structure-aware until this existed first.
