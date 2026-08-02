# Decisions & Learning Log

Dated entries capturing real decisions made on this project and why — not a changelog of code, a record of *reasoning*, so a future reader (including future-me) doesn't have to reconstruct it from scratch. Practice of the "close the loop" pattern (course SLO 3.7): a decision happens, then it gets written down before moving on.

## 2026-07-20 — Python 3.12 over the system Python (3.9.6)

macOS ships Python 3.9.6 as its system Python. It's past its official end-of-life (Oct 2025) and not meant for real development — installing project packages into it risks conflicting with what macOS itself relies on. Installed Python 3.12 via Homebrew and built the project's `.venv` from that instead. Chose 3.12 specifically over the newest (3.14) since some ML libraries we'll need later (sentence-transformers, chromadb) sometimes lag behind brand-new Python releases.

## 2026-07-20 — Raw SQL via `sqlite3`, not an ORM

An ORM (Object-Relational Mapper) would generate SQL for us behind the scenes. Deliberately avoided one — this project exists partly to actually learn SQL, and an ORM would hide exactly the thing being learned.

## 2026-07-21 — `workspace` column instead of full user authentication

Papers need to be separable by who uploaded them (e.g. a friend uploading dengue papers shouldn't mix into a maternal-mortality collection), but full login/auth is explicit non-MVP scope. Solution: a single `workspace` text column on the papers table — one column, many possible values across rows, filtered with `WHERE workspace = '...'`. Scales to any number of people with zero schema changes, unlike a naive "one column per person" spreadsheet-style design. Directly resolves course SLO 4.8 (relational vs. flat data).

## 2026-07-21 — Requirements added incrementally, not front-loaded

`requirements.txt` starts empty. Each dependency gets added at the roadmap step that actually needs it, so its purpose is clear when it's added rather than installing a wall of unused packages on day one.

## 2026-07-23 — Papers schema fields, informed by real bibliographic standards

Researched what real reference managers (Zotero, Mendeley) and metadata standards (Dublin Core, DataCite, CrossRef) actually capture for a paper. Added `journal`, `doi`, and `abstract` beyond the original title/authors/year — `abstract` specifically because it lets the UI show a quick summary without running full RAG retrieval, and `journal`/`doi` because they're what makes a citation look real. Deliberately left out `volume`/`issue`/`pages` (matter for perfect citation formatting, not for retrieval quality) and `keywords` (our retrieval is semantic/embedding-based, not keyword-based, so a keywords column is less load-bearing here than in a traditional reference manager). Schemas are cheap to extend later — this isn't a permanent decision, just the right scope for now.

## 2026-07-23 — `id` (surrogate key) and `doi` (natural key) are both needed

They look redundant but serve different jobs. `id` is internal, always present (auto-assigned on insert), used for relationships between tables later. `doi` is an external, real-world identifier — not guaranteed to exist (many papers don't have one), not something we control, but useful later for detecting duplicate uploads and linking to the original source. Standard database pattern: prefer a surrogate key as the actual primary key even when a natural key exists, because natural keys can be missing or fragile to match on.

## 2026-07-23 — Parameterized queries (`?` placeholders), never string-built SQL

All queries in `app/db/queries.py` pass values as a separate tuple to `.execute()`, never by pasting values directly into the SQL text (e.g. an f-string). Directly pasting user-controlled text into SQL is how SQL injection attacks happen — a paper title containing something like `'; DROP TABLE papers; --` could otherwise be interpreted as a second command instead of a piece of data. Placeholders guarantee values are always treated as data, never as part of the command structure, regardless of their contents.

## 2026-07-24 — `pypdf` for PDF text extraction, chosen over `pdfplumber`

`pypdf` is lightweight and does exactly what we need — extract raw text. `pdfplumber` is more powerful (handles complex layouts and tables precisely) but heavier, and we don't need that level of power for the MVP. Tested against a real academic paper (dengue/climate paper, ~80K characters) — extraction was clean, no garbled text.

**Known limitation, accepted for now:** `pypdf` only extracts text that's actually embedded as selectable text in the PDF. A scanned paper (a photograph of a page, not real typed text) would extract to empty or near-empty output — `pypdf` can't do OCR (recognizing text from an image). Out of scope for the MVP; would need a different tool (e.g. `pytesseract`) if this becomes a real problem with actual uploaded papers.

## 2026-07-28 — Run project files with `-m`, not as a bare script path, once they import our own code

`python app/rag/chunking.py` failed with `ModuleNotFoundError: No module named 'app'` the first time a file tried to import our own project code (`from app.ingestion.pdf_extractor import extract_text`). Running a file directly as a script makes Python search for imports starting from *that file's own folder*, not the project root — so it couldn't find `app/` at all. Fix: run it as a module instead, `python -m app.rag.chunking` (dot notation, no `.py`), which searches starting from the current working directory (the project root) instead. Files that only import third-party/stdlib packages (`schema.py`, `queries.py`, `pdf_extractor.py`) never hit this, since those are always found regardless of the search starting point — this only shows up once a file imports *our own* project structure.

## 2026-07-29 — First real RAG retrieval test: works, with a known weakness

Tested `search()` end-to-end against the real dengue paper with the query "mosquito breeding and rainfall" — deliberately not using the paper's own wording, to test genuine semantic matching rather than keyword overlap. Top result was excellent (found a passage about environmental/climate factors driving dengue, with zero exact word overlap with the query). Results 2-4 were topically relevant but looser matches. Result 5 was a chunk of the paper's *references list*, pulled in because citation entries are dense with topic words ("climate change", "dengue") without being real content.

**Known limitation, consistent with the earlier no-overlap decision:** naive fixed-size chunking has no awareness of document structure, so it can't distinguish real content from a references section. Candidate future fixes: strip reference sections before chunking, or accept this as a real example of RAG's limits for the course's required rag-evaluation.md artifact (SLO 4.22 explicitly wants both successful and failing example queries documented — this is a real failing case, not a hypothetical one).

## 2026-07-29 — Step 4 complete: course review + catch-up artifacts

Ran a 6-question active-recall review (not a lecture — user answered from memory, then corrections were made) covering CLAUDE.md/decisions.md separation, the workspace column design, surrogate vs. natural keys, parameterized queries, chunking, and embeddings. Result: consistently solid grasp of *why* each decision was made; a few precise-vocabulary and one real mechanical gap (initially thought the AI processes every chunk per question, corrected to: retrieval finds a few relevant chunks, generation only ever sees those). Turned the review directly into two course-required artifacts: `docs/db-vocabulary.md` (SLO 4.5, 12 terms) and `docs/data-modeling.md` (SLO 4.8), both written by the user in their own words with assistant fact-checking against the real schema (caught one invented column name, one relational-pattern mismatch, one rows/columns wording slip). This closes out Step 4 end to end: PDF extraction → chunking → embeddings → Chroma storage/search, all built, tested against a real paper, and now also documented against the course.

## 2026-07-31 — Step 5 complete: Streamlit v1, first real button-driven test of the full pipeline

Built `frontend/streamlit_app.py`: a workspace field, an upload form (PDF + metadata), a list of papers already in the workspace, and a raw-retrieval search box (no Claude-generated answer yet — that's Step 6). Three small backend wiring gaps surfaced by actually connecting the pieces for the first time (previously each was only exercised alone via its own `__main__` block):

- `insert_paper()` didn't return anything. The UI needs the new row's ID to tag that paper's chunks in Chroma, so it now returns `cursor.lastrowid` (SQLite hands back the auto-incremented ID right after an insert).
- `get_papers_by_workspace()` returned plain tuples, so reading a field meant a brittle positional index (`paper[1]`). Switched to `connection.row_factory = sqlite3.Row`, so callers can use `paper["title"]` instead — same data, safer to read, unaffected by future column reordering.
- Streamlit runs `frontend/streamlit_app.py` directly (never with `-m`), which hits the exact `ModuleNotFoundError` described in the 2026-07-28 entry above, since Python only knows about `frontend/`'s own folder by default. Fixed the same way: explicitly add the project root to `sys.path` at the top of the file (`sys.path.insert(0, str(Path(__file__).resolve().parent.parent))`) instead of relying on `-m`, which isn't available for how Streamlit invokes scripts.

Verified end-to-end in an actual browser (headless Chromium via Playwright, not just import-and-call): uploaded `data/sample.pdf`, got a success message with a real chunk count (81), saw it appear in the paper list, and ran a semantic search query that returned real matching text with distance scores. One real (harmless) surprise during testing: a raw `.fill()` into the search box produced zero results until the field lost focus — Streamlit's `st.text_input` only triggers a script rerun on blur or Enter, not on every keystroke, same category of "nothing happens until a deliberate submit" behavior as the upload form's submit button, just implicit here instead of an explicit form.

**Note on architecture, relevant to course SLO 4.19 (frontend vs. backend):** at this step, `streamlit_app.py` calls `app/db`, `app/ingestion`, and `app/rag` functions directly, in-process — there's no HTTP boundary yet. `app/api/` (the FastAPI layer) is still Step 6+, per `docs/project-structure.md`. This is an intentional in-between architecture, not a shortcut to fix later.

## 2026-07-31 — SLO 4.19 (frontend vs. backend) satisfied via recall quiz

Ran a 5-question active-recall quiz on the architecture built in Step 5 — what frontend/backend mean here, what HTTP is, why the current in-process setup has no boundary yet, and why that boundary would eventually matter. Answers were mostly solid from memory; one real misconception corrected: initial instinct was that separating frontend/backend would make things "faster and more efficient" — actually backwards, since an HTTP call has more overhead than a direct in-process function call. The real reasons (reusability across multiple frontends, independent deployment, a single security gate) were understood once corrected. Turned the corrected understanding directly into `docs/system-architecture.md`, written by the user in their own words, assistant fact-checked against the real `frontend/streamlit_app.py` (caught one inaccuracy: described clicking a "search tab," but the actual UI has no `st.tabs` — it's one continuous scrolling page). Diagram section left unfilled by choice; not required to close the SLO.

## 2026-07-31 — SLO 4.7 (critically evaluate DB decisions) satisfied

Compiled `docs/db-review-log.md`: 4 historical cases already noted in `course-alignment.md` (workspace-column pushback, invented `topic` column caught, relational-pattern mismatch caught, SLO 4.6 self-correction), plus one new live case. For the new one, two Step 5 decisions were put up for real-time questioning instead of being accepted on sight: whether `insert_paper` returning `lastrowid` could ever be wrong (it can't, in this code, because the same connection files and reads it immediately — but only in this code, not as a universal fact), and whether switching `get_papers_by_workspace` to `sqlite3.Row` was actually necessary (no — plain tuples would've worked, `Row` is a safety/readability upgrade, and it doesn't affect *which* rows come back, only how their fields get read afterward). First explanation of both used jargon ("scoped to the connection," "stale value") that didn't land — redone with a filing-cabinet/name-tag analogy instead, which did.

## 2026-08-01 — Step 6 complete: RAG Q&A, the centerpiece, working end to end

Built the actual "ask a question, get a real answer" feature. Before writing code, had the user (a complete beginner) describe in plain English what the prompt to Claude should do — the answer was essentially the full spec already: use only the given excerpts, no outside knowledge, cite the paper, say "I don't know" instead of guessing. That became the system prompt almost verbatim; the only new API concept needed was the system/user message split (background instructions vs. the specific question).

**Citations required a real design decision, not just string interpolation.** First instinct was to store each chunk's paper *title* directly in Chroma alongside the chunk text. Caught before implementing: this would duplicate data that already lives in `papers.db` (title, authors, year), the same "two sources of truth" problem the `workspace`-column design was built to avoid back in Step 2. Fixed by storing each chunk's `paper_id` in Chroma instead (a real, queryable metadata field — previously only implicit in the id string like `"1-3"`), and adding `get_paper_by_id()` to `app/db/queries.py` so `generate_answer()` looks up the real title/authors/year at answer time. Citations now read like `"Climate Drivers of Dengue Transmission in Pakistan — A. Khan, S. Ahmed (2022)"` instead of a bare title.

**Environment/secrets setup (SLO 4.20, 4.21):** created `.env` (real key, gitignored) and `.env.example` (placeholder, safe to commit) and verified the key worked with a live "say hello" test call before building anything on top of it. Real near-miss during setup: after being told to revoke and regenerate the key, the user pasted the *new* key into `.env.example` instead of `.env` — the exact inversion of what the two files are for. Caught immediately (checked `git status`: the file was untracked, so nothing was ever exposed) and fixed by swapping the two files' contents. Concrete evidence that "can restate the rule" and "hands do the right thing under low attention" are different stages of learning — not a knowledge gap, a not-yet-automatic-habit gap.

**Cost check before building:** estimated ~$0.02/query on `claude-opus-4-8` (the CLAUDE.md default) given ~5 retrieved chunks (~5,000 characters ≈ 1,500–2,000 input tokens) plus a short cited answer (~200–300 output tokens) — meaning even 500 test queries would cost under $10. Considered Haiku for cost savings but kept Opus, since SLO 4.22 (this exact RAG-evaluation SLO) explicitly wants documented failing queries, and a cheaper model would blur "retrieval found the wrong chunks" (an interesting, real RAG limitation worth documenting) vs. "the model just isn't very good at following the citation instructions" (not what's being tested here).

**Verified in an actual browser**, not just a Python `__main__` block: asked "What is the economic burden of dengue?" against the real uploaded paper. Claude answered by quoting the paper directly, cited it correctly in the "Author, Year" format, and — for the part of the question the paper didn't have a specific number for — said so honestly instead of inventing a figure. That last part is the whole point of RAG's grounding instruction actually working, confirmed with a real query, not assumed from the code.

`docs/course-alignment.md`: SLO 4.22 (RAG for document Q&A) updated — extraction, chunking, embeddings, retrieval, *and* Claude-generated cited answers are now all built and verified end to end. `docs/rag-evaluation.md` (10+ documented queries, 5 working + 3 failing) still not written — that's the remaining artifact, not the underlying capability.

## 2026-08-03 — SLO 4.20 (what an API is) satisfied

Ran a 4-question recall quiz on API concepts, tied to the real Claude API call built in Step 6. Three of four answers were solid from memory, including a genuinely sharper version of the restaurant analogy than the one originally given (waiter as the API itself, actively relaying and returning, rather than a static menu). One real correction: described "code" as being shared between the two computers during an API call — corrected to "a message/data," since the actual Python code never leaves the local machine; only the request text and response text travel over the network. Turned the corrected answers directly into `docs/api-test.md`, written by the user in their own words.

## 2026-08-03 — SLO 4.21 (env variables) satisfied

Ran a 3-question recall quiz on env-variable security, using the real `.env`/`.env.example` mixup from Step 6 as the worked example. Two of three answers were correct outright. One sharpened: initially framed "the mistake was fixed" as the same thing as "we confirmed nothing leaked" — corrected to separate the two claims. Editing the file fixes it going forward; the actual proof of safety was running `git status` and seeing the file was untracked (never committed or pushed). If it had already been pushed, editing afterward wouldn't undo the exposure — the key would still need revoking regardless. Turned the corrected answers directly into `docs/env-security.md`, written by the user in their own words.

## 2026-08-03 — SLO 4.22 (`rag-evaluation.md`) deferred, explicit reason

Before writing the centerpiece evaluation artifact, hit a real scope ambiguity in the SLO's own wording: "10+ docs, 5 working + 3 failing queries documented" could mean 10+ *uploaded papers* to test against, or just 10+ *documented query results*. The workspace currently only has one real paper (uploaded twice under different filenames), so the honest answer either way was "not ready yet." Decision: defer the whole artifact rather than write a thin version against one paper — go download ~10 real papers first, then run and document the full eval against a real multi-paper corpus. The underlying RAG capability itself is already done and verified (2026-08-01); only the evaluation writeup is deferred. **Explicit reminder to pick this back up in a future session once more papers are uploaded** — see the updated status in `docs/course-alignment.md`.

## 2026-08-03 — Phase 1–3 course status corrected: a 2-week drift, caught by the user

Auditing `docs/course-alignment.md` (prompted by the user directly asking "are we actually applying Phase 1–3 material?"), found that a decision from 2026-07-20 — mark Phase 1–3 SLOs "satisfied in prior project" rather than "Not started," since the user genuinely completed those phases before this repo existed — was agreed but never actually written into the file. The rows sat as "Not started" through Steps 4, 5, and 6, which is exactly what surfaced the question today. Corrected every Phase 1–3 row accordingly, and verified two things for real while auditing: `CLAUDE.md`'s own git history (4 commits so far, several more from this session not yet committed) and its line count (48 lines — genuinely under the 100-line target, no refactoring needed).

Standing decision going forward: no dedicated artifacts for Phase 1–3 in this repo — that's settled, not "later." Instead, per a new rule in `CLAUDE.md`'s Preferences section, proactively call out in the moment whenever current work is genuinely applying a Phase 1–3 concept (closing the loop, context window awareness, producer vs. consumer mindset, this project's real dual-layer memory architecture) — awareness instead of a checklist. The real lesson from the drift itself: write a "decided" item into the actual tracked file in the same turn it's decided, not as a promise to apply later — that gap is exactly what let this go stale for two weeks.

## 2026-07-24 — Fixed-size chunking, no overlap (for now)

`chunk_text()` splits paper text into equal-sized pieces with no overlap between them. A more refined technique gives neighboring chunks a bit of shared overlap, so a sentence that would otherwise get cut in half at a chunk boundary still appears in full somewhere. Deliberately skipped for now to keep Step 4 (already the densest step on the roadmap) from getting even more complex on the first pass. Revisit if retrieval quality later seems to miss things right at chunk boundaries — this file isn't committed yet, still mid-Step-4.
