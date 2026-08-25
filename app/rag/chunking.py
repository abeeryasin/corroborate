"""Splits cleaned Markdown text into chunks along real paragraph
boundaries, instead of blindly cutting every N characters. Depends on
text that's already been through app.ingestion.text_cleaner — raw
pypdf output has no reliable paragraph signal to split on (see
docs/decisions.md).
"""


def chunk_text(text, chunk_size=1000):
    paragraphs = _merge_headings_with_content(
        [p.strip() for p in text.split("\n\n") if p.strip()]
    )

    chunks = []
    current = ""
    for para in paragraphs:
        if len(para) > chunk_size:
            if current:
                chunks.append(current)
                current = ""
            chunks.extend(_split_long_paragraph(para, chunk_size))
        elif len(current) + len(para) <= chunk_size:
            current = f"{current}\n\n{para}" if current else para
        else:
            chunks.append(current)
            current = para

    if current:
        chunks.append(current)

    return chunks


def _merge_headings_with_content(paragraphs):
    """Glues a heading — or a run of consecutive headings, e.g. a section
    title immediately followed by a subsection title — to the first real
    paragraph that follows, so a chunk boundary can never land between a
    heading and its own content."""
    merged = []
    i = 0
    while i < len(paragraphs):
        group = [paragraphs[i]]
        while group[-1].startswith("#") and i + 1 < len(paragraphs):
            i += 1
            group.append(paragraphs[i])
        merged.append("\n\n".join(group))
        i += 1
    return merged


def _split_long_paragraph(paragraph, chunk_size):
    """Fallback for a single paragraph bigger than chunk_size on its own —
    splits at sentence boundaries instead of a blind character cut."""
    sentences = paragraph.split(". ")

    chunks = []
    current = ""
    for i, sentence in enumerate(sentences):
        piece = sentence if sentence.endswith((".", "!", "?")) or i == len(sentences) - 1 else sentence + "."
        if len(current) + len(piece) <= chunk_size or not current:
            current = f"{current} {piece}" if current else piece
        else:
            chunks.append(current)
            current = piece

    if current:
        chunks.append(current)

    return chunks


if __name__ == "__main__":
    from app.ingestion.pdf_extractor import extract_text
    from app.ingestion.text_cleaner import clean_to_markdown

    raw = extract_text("data/sample.pdf")
    cleaned = clean_to_markdown(raw)
    chunks = chunk_text(cleaned)
    print(f"Split into {len(chunks)} chunks")
    print(f"Chunk sizes: min={min(len(c) for c in chunks)}, max={max(len(c) for c in chunks)}")
    print(chunks[0])
