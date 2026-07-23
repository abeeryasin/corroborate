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
