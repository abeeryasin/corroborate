"""Tests for app.rag.vector_store.search() — verifies the diversity-cap
fix (docs/rag-evaluation.md failure #2: one paper crowding out a
different relevant paper) stays fixed. Uses the real local Chroma
collection and local embedding model — no Claude API calls, no cost.
"""

import pytest

from app.rag.vector_store import add_chunks, search, collection

TEST_WORKSPACE = "_pytest_diversity_test"


@pytest.fixture(autouse=True)
def cleanup():
    yield
    collection.delete(where={"workspace": TEST_WORKSPACE})


def test_search_caps_results_per_paper_and_does_not_crowd_out_a_minority_paper():
    dominant_chunks = [f"Paper A discusses TAK-003 immune response detail number {i}." for i in range(8)]
    add_chunks(dominant_chunks, paper_id=90001, workspace=TEST_WORKSPACE)
    add_chunks(["Paper B also discusses TAK-003 immune response briefly."], paper_id=90002, workspace=TEST_WORKSPACE)

    results = search("TAK-003 immune response", workspace=TEST_WORKSPACE, n_results=5, max_per_paper=2)
    paper_ids = [m["paper_id"] for m in results["metadatas"][0]]

    assert paper_ids.count(90001) <= 2
    assert 90002 in paper_ids
