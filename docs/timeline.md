# Timeline Estimate

Rough hours per roadmap step, at a beginner's pace, assuming ~3 hrs/day.

**Important scope note:** this is an estimate for the *project build steps* (1–9 below), not a separate estimate for the course's own weekly phases. Since we merged the two tracks — learning the curriculum concepts *through* the project instead of as a separate track (see `docs/course-alignment.md`) — there's no clean "Phase 1 = X hours" figure anymore. The course's original pasted material listed its own rough week-by-week hour budgets (e.g. "Week 1, ~8–10 hrs"), but those numbers assumed doing the course's own standalone exercises, which isn't what we're doing. Use the table below as the real estimate.

| Step | What it is | Est. hours | Why |
|---|---|---|---|
| 1 | Scaffold | 2–4 | Mostly setup/tooling, not much new logic — **done** |
| 2 | Metadata DB | 6–9 | New: SQL fundamentals, schema design |
| 3 | PDF ingestion | 3–6 | File I/O, a new library, edge cases (scanned PDFs won't extract) |
| 4 | Chunking + embeddings | 6–9 | Densest new-concept step: chunking, embeddings, vector search all at once |
| 5 | Streamlit v1 | 2–3 | Streamlit is quick once Python is comfortable |
| 6 | RAG Q&A | 9–12 | The centerpiece — ties everything together, most debugging |
| 7 | Polish | 3–6 | Tests, error handling, README |
| 8 | Deploy | 6–9 | Usually harder than expected — persistent storage, env config |
| 9 | Light eval | 2–3 | Small, mechanical once the pipeline works |
| **Total** | | **~40–60 hrs** | |

At 3 hrs/day, that's roughly **4–7 weeks of calendar time** — not because the raw work takes that long, but because beginner estimates run long in a specific, predictable direction: debugging and genuinely understanding (not just copying) takes longer than a working engineer solo would need. Treat this as a rough shape, not a deadline. If Step 4 or Step 6 takes longer than planned, that's not a problem — that's where the real learning is happening.

## Deferred work (not counted above)

- v2 features (study comparison, evidence tables, gap identification, decision tracking, agents, knowledge-graph exercise) — no estimate yet, will be scoped when we get there.
- v3 idea: automatic literature search via PubMed/Semantic Scholar APIs — same, unscoped until relevant.
- Course SLOs reclassified as "solo-adaptable" in `docs/course-alignment.md` (guardrails, observability, staging, etc.) — folded into Steps 6–9 above where they fit; not separately budgeted.
