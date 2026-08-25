"""Tests for the deterministic parts of app.ingestion.text_cleaner — the
batching logic only. Whether the LLM's cleaned output is actually good
isn't something a deterministic test can check (that's a judgment call
about text quality, not a pass/fail condition) — that's what
docs/rag-evaluation.md's manual verification is for, a genuinely
different kind of testing. These tests never call the Claude API, so
they're free and instant.
"""

from app.ingestion.text_cleaner import _split_into_batches


def test_short_text_is_a_single_batch():
    assert _split_into_batches("short text", batch_size=100) == ["short text"]


def test_splits_into_correct_number_of_batches():
    text = "x" * 250
    batches = _split_into_batches(text, batch_size=100)
    assert [len(b) for b in batches] == [100, 100, 50]


def test_batches_reconstruct_the_original_text_exactly():
    text = "Some real text content, not a round number of characters long."
    batches = _split_into_batches(text, batch_size=17)
    assert "".join(batches) == text
