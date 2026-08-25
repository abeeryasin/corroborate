"""Tests for app.rag.chunking — verifies the real bugs found in
docs/rag-evaluation.md, and fixed this session, stay fixed: no
mid-sentence cuts, and no section heading stranded without its content.
"""

from app.rag.chunking import chunk_text, _merge_headings_with_content, _split_long_paragraph


def test_short_text_is_one_chunk():
    assert chunk_text("Just one short paragraph.") == ["Just one short paragraph."]


def test_no_chunk_ends_mid_sentence():
    paragraphs = [f"Paragraph number {i} has some real sentence content in it." for i in range(30)]
    text = "\n\n".join(paragraphs)
    chunks = chunk_text(text, chunk_size=200)
    for chunk in chunks:
        ending = chunk.rstrip()[-1]
        assert ending in ".!?:", f"chunk ended mid-sentence: ...{chunk[-40:]!r}"


def test_heading_stays_glued_to_its_content_paragraph():
    merged = _merge_headings_with_content(["## Introduction", "This is the actual introduction text."])
    assert merged == ["## Introduction\n\nThis is the actual introduction text."]


def test_consecutive_headings_all_merge_with_the_real_content():
    # the exact real bug: a section heading immediately followed by a
    # subsection heading, with the real content one step further away
    merged = _merge_headings_with_content(["## Methods", "### Data sources", "We used real data for this analysis."])
    assert merged == ["## Methods\n\n### Data sources\n\nWe used real data for this analysis."]


def test_trailing_heading_with_no_content_stays_alone():
    # a heading really can end up alone if it's the very last paragraph
    # in the whole document — nothing to glue it to, and that's correct
    merged = _merge_headings_with_content(["Some final paragraph.", "## References"])
    assert merged == ["Some final paragraph.", "## References"]


def test_oversized_paragraph_falls_back_to_sentence_split():
    long_paragraph = "This is a sentence. " * 100
    pieces = _split_long_paragraph(long_paragraph, chunk_size=100)
    assert all(len(p) <= 150 for p in pieces)
    for p in pieces:
        assert p.rstrip()[-1] in ".!?"
