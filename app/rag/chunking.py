"""Splits extracted paper text into fixed-size chunks."""


def chunk_text(text, chunk_size=1000):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks


if __name__ == "__main__":
    from app.ingestion.pdf_extractor import extract_text

    text = extract_text("data/sample.pdf")
    chunks = chunk_text(text)
    print(f"Split into {len(chunks)} chunks")
    print(chunks[0])
