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


def init_db():
    connection = sqlite3.connect(DB_PATH)
    connection.execute(CREATE_PAPERS_TABLE)
    connection.commit()
    connection.close()


if __name__ == "__main__":
    init_db()
    print(f"Database ready at {DB_PATH}")
