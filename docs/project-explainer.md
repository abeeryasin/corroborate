# Corroborate — Project Explainer (plain-language, beginner-level)

A companion to `docs/system-architecture.md`, `docs/decisions.md`, and `README.md` — this synthesizes those into one plain-language read, with the reasoning behind the reasoning where it matters.

## What this project actually is

Upload research papers, ask a question in plain English, get an answer grounded in *your specific uploaded papers* — with the exact source cited, and an honest "I don't know" instead of a guess when the answer isn't actually there. The problem it solves: reviewing literature usually means re-reading papers to re-find a fact you already found once. Think of it as a research assistant with a genuinely honest memory — one who only ever tells you things they actually read in your files, and admits when they don't know.

## Architectural decisions — the "why"

- **Raw SQL, not an ORM.** An ORM writes SQL for you behind the scenes. Skipped deliberately — this project exists partly to actually learn SQL, and hiding it would hide the thing being learned.
- **`workspace` column, not real login/accounts.** One text column, filtered with `WHERE workspace = '...'`, scales to any number of "folders" with zero database redesign. Deliberately not real security — see Limitations below.
- **Two IDs that look redundant but aren't.** An internal `id` (always exists, links tables together) and a `doi` (a real-world identifier many papers don't even have). The internal ID is the one actually relied on, since the "real" one can be missing.
- **Parameterized queries, never pasted-together SQL.** Values are always passed separately from the SQL text — the actual defense against SQL injection, not a theoretical concern.
- **`pypdf`, not `pdfplumber`.** Chosen twice, for two different reasons, and lost both times. First (Step 3): `pdfplumber` is more powerful — precise layout/table reading — but that precision wasn't needed to just extract raw text, and `pypdf` tested clean. Second (this session): `pdfplumber`'s exact strength — reading position/spacing data — was the *free* alternative to the LLM-based cleanup step, considered specifically because of a real budget concern. Once real pricing came back under $2 for a portfolio piece, the LLM version was chosen instead.
- **No frontend/backend split (no FastAPI).** Right now it's one Python program calling its own functions directly — not separate buildings you call over the internet. A FastAPI layer was scaffolded early, sat unused, and was deliberately deleted rather than left as a misleading placeholder. **Precisely:** this boundary matters when a *second consumer* (another frontend, a mobile app, an external script) needs to call the same logic over HTTP — there's only ever been one frontend, so that need never existed. It is **not** primarily about supporting more simultaneous users — that's a separate scaling question a backend split doesn't automatically solve either.
- **Two different databases, two different jobs.** SQLite holds structured facts (title, authors, year). Chroma holds the paper text as searchable "meaning vectors." Neither is good at the other's job.
- **Embeddings run locally, not through an API.** No per-search network cost — unlike the answer-generation step, which does call Claude.

## The workflow — what actually happens end to end

1. **Extract** — `pypdf` pulls raw text out of the PDF, with no structure preserved (confirmed directly this session: real paragraph breaks don't exist in the raw output — every line break looks the same whether it's a real paragraph break or a mid-sentence wrap).
2. **Clean** *(added this session)* — Claude rewrites the messy raw text into structured Markdown, fixing headers/footers bleeding into sentences and restoring real paragraph breaks. Processed in batches of **20,000 characters** (`BATCH_SIZE` in `text_cleaner.py` — raised from an initial 8,000 to cut the number of API round-trips), run in parallel instead of one after another.
3. **Chunk** — the clean text is split into pieces for storage/retrieval, still **1,000 characters** (`chunk_size` in `chunking.py` — this number never changed), but now cut along real paragraph boundaries instead of a blind character count, and never leaving a section heading stranded without its content.
4. **Embed & store** — each chunk becomes a vector (numbers capturing meaning, not just words), stored in Chroma, tagged with which paper it came from.
5. **Search** — the question also becomes a vector; Chroma finds the closest-meaning chunks, capped at 2 per paper so one paper can't crowd out a different relevant one.
6. **Generate** — the retrieved chunks (not the whole paper) go to Claude with a strict instruction: answer only from these excerpts, cite the paper, say "I don't know" rather than guess.

**Don't confuse the two size numbers:** `BATCH_SIZE` (20,000, in the cleaning step) and `chunk_size` (1,000, in the chunking step) live in different files and do different jobs — one controls how much text is cleaned per API call, the other controls the size of the pieces actually stored and retrieved.

## Pros

- Grounded, not hallucinated — real citations, a genuine "I don't know" path.
- Genuinely evaluated, not just demoed — `docs/rag-evaluation.md` documents real successes *and* real, root-caused failures.
- Simple enough to actually understand — no ORM magic, no distributed system, one Python program traceable top to bottom.
- Every non-trivial choice has a written, dated reason (`docs/decisions.md`), not a vibe.

## Cons and real limitations

- **No automated test suite yet** — `tests/` exists but is a placeholder. What's been done so far is *manual* structured testing (e.g. checking chunk boundaries and diversity-cap results by hand, once, on request). An automated suite means writing those same checks as permanent code (using `pytest`) that runs by itself on demand — the difference isn't sophistication, it's that a manual check proves something worked *once*, an automated test proves it *keeps* working.
- **Ephemeral storage on the deployed version** — the free hosting tier wipes local files on sleep/redeploy. The real corpus lives safely on the local machine; the deployed copy is a demo, not permanent storage.
- **`workspace` is a label, not security** — on the live deployed app, anyone with the URL could see or delete *any* workspace's papers. Fine for a solo demo, a real problem the moment more than one person actually depends on it.
- **`pypdf` can't read scanned documents** — only works on PDFs with real, selectable text underneath.
- **Retrieval is still capped at a handful of chunks per question** — even with the diversity fix, a question needing very deep coverage of one huge document can come up short.
- **No automated alerting** — the System Health dashboard shows real numbers, but nothing pages a human if something breaks.
