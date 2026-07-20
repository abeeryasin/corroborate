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
