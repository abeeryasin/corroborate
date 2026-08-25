"""Tests for app.db.queries and app.db.schema — real SQLite operations
against a fresh, temporary database file, never the real data/papers.db.
"""

import sqlite3

import pytest

from app.db import schema, queries


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    db_path = str(tmp_path / "test_papers.db")
    monkeypatch.setattr(schema, "DB_PATH", db_path)
    monkeypatch.setattr(queries, "DB_PATH", db_path)
    schema.init_db()
    return db_path


def _insert(workspace="test-ws", title="Test Paper"):
    return queries.insert_paper(
        title=title, authors="A. Author", year=2024, journal="Test Journal",
        doi=None, abstract="An abstract.", workspace=workspace,
        filename="test.pdf", uploaded_at="2026-01-01T00:00:00",
    )


def test_insert_paper_returns_a_real_id(temp_db):
    paper_id = _insert()
    assert isinstance(paper_id, int)
    assert paper_id > 0


def test_get_papers_by_workspace_only_returns_that_workspace(temp_db):
    _insert(workspace="ws-1", title="Paper A")
    _insert(workspace="ws-2", title="Paper B")

    papers = queries.get_papers_by_workspace("ws-1")
    assert len(papers) == 1
    assert papers[0]["title"] == "Paper A"


def test_delete_paper_actually_removes_it(temp_db):
    paper_id = _insert()
    queries.delete_paper(paper_id)
    assert queries.get_paper_by_id(paper_id) is None


def test_update_paper_changes_the_right_fields(temp_db):
    paper_id = _insert(title="Old Title")
    queries.update_paper(paper_id, title="New Title", authors="New Author", year=2021,
                          journal="New Journal", doi="10.1/x", abstract="New abstract")
    updated = queries.get_paper_by_id(paper_id)
    assert updated["title"] == "New Title"
    assert updated["year"] == 2021


def test_question_log_stats_aggregate_correctly(temp_db):
    queries.log_question(workspace="ws", question="Q1", response_time_seconds=1.5,
                          was_error=False, was_dont_know=False,
                          asked_at="2026-01-01T00:00:00", cost_usd=0.01)
    queries.log_question(workspace="ws", question="Q2", response_time_seconds=2.5,
                          was_error=False, was_dont_know=True,
                          asked_at="2026-01-01T00:01:00", cost_usd=0.02)

    stats = queries.get_question_stats("ws")
    assert stats["total_questions"] == 2
    assert stats["dont_know_count"] == 1
    assert round(stats["total_cost"], 2) == 0.03


def test_init_db_adds_cost_usd_column_to_a_pre_existing_question_log(tmp_path, monkeypatch):
    # regression test for a real documented gotcha (docs/decisions.md):
    # CREATE TABLE IF NOT EXISTS only fires for brand-new databases, so an
    # existing question_log table needs the new column added separately.
    db_path = str(tmp_path / "legacy.db")
    monkeypatch.setattr(schema, "DB_PATH", db_path)

    connection = sqlite3.connect(db_path)
    connection.execute("""
        CREATE TABLE question_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workspace TEXT NOT NULL,
            question TEXT NOT NULL,
            response_time_seconds REAL,
            was_error INTEGER NOT NULL,
            was_dont_know INTEGER NOT NULL,
            asked_at TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()

    schema.init_db()

    connection = sqlite3.connect(db_path)
    columns = [row[1] for row in connection.execute("PRAGMA table_info(question_log)")]
    connection.close()
    assert "cost_usd" in columns
