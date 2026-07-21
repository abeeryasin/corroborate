# Project Structure

What exists right now, what each piece is for, and which roadmap step fills it in.

```
Research/
├── .venv/                    Private Python environment (gitignored — not in the repo)
├── .gitignore
├── CLAUDE.md                 Project handbook — read by every future coding session
├── README.md                 Human-facing intro
├── requirements.txt          Currently empty — grows as each step needs a package
│
├── app/                      The actual backend application
│   ├── __init__.py             (marks app/ as an importable Python package)
│   ├── api/                    FastAPI route handlers — Step 6+. The endpoints
│   │                           the frontend calls: "upload a paper", "ask a question"
│   ├── db/                     SQLite schema + raw SQL — Step 2, next up.
│   │                           Everything about storing/reading paper metadata
│   ├── ingestion/               PDF → text → chunks — Steps 3–4.
│   │                           Reading uploaded PDFs, preparing them for embedding
│   └── rag/                     Retrieval + Claude generation — Step 6, the centerpiece.
│                               Embed the question, pull relevant chunks from Chroma,
│                               build the prompt, call Claude
│
├── frontend/                  Currently empty — gets streamlit_app.py at Step 5
│
├── data/                       Generated at runtime, gitignored
│   └── .gitkeep                 The actual SQLite file and Chroma's vector store will
│                               live here once the app runs — this is output, not code
│
├── tests/                      Automated tests — Step 7
│   └── __init__.py
│
└── docs/
    ├── decisions.md            The "why" log
    ├── course-alignment.md     Course-SLO mapping
    ├── project-structure.md    This file
    └── timeline.md             Hour/time estimates per roadmap step
```

## Notes

- **`app/`, `app/api/`, `app/db/`, `app/ingestion/`, `app/rag/`, and `tests/` each currently hold only an `__init__.py`** — empty except for that one file. This is intentional, not incomplete: `__init__.py` is what makes a folder importable as a Python package. Actual logic files get added folder-by-folder as we reach the roadmap step that needs them.
- **There's no `app/main.py` yet.** That will be the FastAPI entrypoint tying `api/`, `db/`, `ingestion/`, and `rag/` together — it doesn't exist yet because there's nothing to wire together until those pieces exist.
- **`frontend/` isn't in Git yet.** Git doesn't track empty folders, so it exists on disk but won't appear in the repo until `streamlit_app.py` lands in it at Step 5.

The folder structure *is* the roadmap, laid out physically — each empty folder is a placeholder for an already-agreed step, not a guess at future needs.
