"""Bulk-ingest a folder of PDFs into a workspace — the same pipeline the
Streamlit upload form uses (extract -> auto-detect metadata -> chunk ->
embed), but for many papers at once from the command line instead of
one at a time through the browser.

Usage: python scripts/ingest_papers.py <folder> <workspace>
"""

import datetime
import glob
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db.queries import insert_paper
from app.ingestion.pdf_extractor import extract_text
from app.ingestion.metadata_extractor import extract_metadata
from app.ingestion.text_cleaner import clean_to_markdown
from app.rag.chunking import chunk_text
from app.rag.vector_store import add_chunks


def ingest_folder(folder, workspace):
    for pdf_path in sorted(glob.glob(os.path.join(folder, "*.pdf"))):
        filename = os.path.basename(pdf_path)
        print(f"Ingesting {filename}...")

        text = extract_text(pdf_path)
        metadata = extract_metadata(text)
        cleaned_text = clean_to_markdown(text)
        chunks = chunk_text(cleaned_text)

        paper_id = insert_paper(
            title=metadata["title"] or filename,
            authors=metadata["authors"] or None,
            year=int(metadata["year"]) if metadata["year"].strip() else None,
            journal=metadata["journal"] or None,
            doi=metadata["doi"] or None,
            abstract=metadata["abstract"] or None,
            workspace=workspace,
            filename=filename,
            uploaded_at=datetime.datetime.now().isoformat(),
        )
        add_chunks(chunks, paper_id=paper_id, workspace=workspace)
        print(f"  -> paper_id={paper_id}, title='{metadata['title']}', {len(chunks)} chunks")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scripts/ingest_papers.py <folder> <workspace>")
        sys.exit(1)
    ingest_folder(sys.argv[1], sys.argv[2])
