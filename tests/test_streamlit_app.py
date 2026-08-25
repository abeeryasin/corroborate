"""Tests for frontend/streamlit_app.py using Streamlit's own AppTest tool
— runs the real script without a browser. Uses a temporary database
(never the real data/papers.db, same technique as test_db_queries.py);
mocks generate_answer() so this never calls the real Claude API or
spends money.
"""

from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from app.db import schema, queries


def _prepare_temp_db(tmp_path, monkeypatch):
    db_path = str(tmp_path / "test_papers.db")
    monkeypatch.setattr(schema, "DB_PATH", db_path)
    monkeypatch.setattr(queries, "DB_PATH", db_path)
    schema.init_db()
    queries.insert_paper(
        title="Test Paper", authors="A. Author", year=2024, journal="Test Journal",
        doi=None, abstract="An abstract.", workspace="test-ws",
        filename="test.pdf", uploaded_at="2026-01-01T00:00:00",
    )


# The embedding model's cold-start load (documented in .claude/skills/launch-app/
# SKILL.md) is slower than AppTest's default 3s timeout on the first script run.
COLD_START_TIMEOUT = 30


def test_app_loads_without_crashing(tmp_path, monkeypatch):
    _prepare_temp_db(tmp_path, monkeypatch)
    at = AppTest.from_file("frontend/streamlit_app.py")
    at.run(timeout=COLD_START_TIMEOUT)
    assert not at.exception


def test_workspace_selector_shows_real_workspaces(tmp_path, monkeypatch):
    _prepare_temp_db(tmp_path, monkeypatch)
    at = AppTest.from_file("frontend/streamlit_app.py")
    at.run(timeout=COLD_START_TIMEOUT)
    assert "test-ws" in at.selectbox[0].options


def test_asking_a_question_displays_the_mocked_answer(tmp_path, monkeypatch):
    _prepare_temp_db(tmp_path, monkeypatch)
    with patch(
        "app.rag.generation.generate_answer",
        return_value=("A mocked cited answer.", ["Test Paper — A. Author (2024)"]),
    ):
        at = AppTest.from_file("frontend/streamlit_app.py")
        at.run(timeout=COLD_START_TIMEOUT)
        # The upload form's own text_inputs (Title, Authors, Year, Journal, DOI)
        # render before "Question" in script order, even collapsed inside an
        # expander — find the real question box by its label, not by position.
        question_box = next(w for w in at.text_input if w.label == "Question")
        question_box.input("What is this paper about?").run(timeout=COLD_START_TIMEOUT)

    rendered_text = " ".join(el.value for el in at.markdown)
    assert "A mocked cited answer." in rendered_text
