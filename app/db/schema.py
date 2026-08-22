"""Creates the papers table if it doesn't already exist."""

import sqlite3

DB_PATH = "data/papers.db"

CREATE_PAPERS_TABLE = """
CREATE TABLE IF NOT EXISTS papers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    authors TEXT,
    year INTEGER,
    journal TEXT,
    doi TEXT,
    abstract TEXT,
    workspace TEXT NOT NULL,
    filename TEXT,
    uploaded_at TEXT NOT NULL
);
"""

CREATE_QUESTION_LOG_TABLE = """
CREATE TABLE IF NOT EXISTS question_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workspace TEXT NOT NULL,
    question TEXT NOT NULL,
    response_time_seconds REAL,
    was_error INTEGER NOT NULL,
    was_dont_know INTEGER NOT NULL,
    asked_at TEXT NOT NULL,
    cost_usd REAL
);
"""


def init_db():
    connection = sqlite3.connect(DB_PATH)
    connection.execute(CREATE_PAPERS_TABLE)
    connection.execute(CREATE_QUESTION_LOG_TABLE)

    # Migration: question_log already existed (with real data) before cost_usd
    # was added. CREATE TABLE IF NOT EXISTS above only fires for brand-new
    # databases, so existing ones need the column added separately.
    existing_columns = [row[1] for row in connection.execute("PRAGMA table_info(question_log)")]
    if "cost_usd" not in existing_columns:
        connection.execute("ALTER TABLE question_log ADD COLUMN cost_usd REAL")

    connection.commit()
    connection.close()


if __name__ == "__main__":
    init_db()
    print(f"Database ready at {DB_PATH}")
