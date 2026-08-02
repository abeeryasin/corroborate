"""Step 5: Streamlit UI — upload papers, list them, and test raw retrieval.

No Claude-generated answers yet (that's Step 6). This page proves the
extract -> chunk -> embed -> store -> search pipeline works end to end
through buttons instead of typed Python commands.
"""

import datetime
import os
import sys
from pathlib import Path

# Streamlit runs this file directly (not with `-m`), so Python only knows
# about frontend/'s own folder by default and can't find `app.*`. Same root
# cause as the ModuleNotFoundError in docs/decisions.md (2026-07-28) — fix
# it the same way, by putting the project root on the import search path.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from app.db.schema import init_db
from app.db.queries import insert_paper, get_papers_by_workspace
from app.ingestion.pdf_extractor import extract_text
from app.rag.chunking import chunk_text
from app.rag.vector_store import add_chunks
from app.rag.generation import generate_answer

init_db()

st.title("Evidence Intelligence Platform")

workspace = st.text_input("Workspace", value="abeer-test")

st.header("Upload a paper")
with st.form("upload_form", clear_on_submit=True):
    uploaded_file = st.file_uploader("PDF file", type="pdf")
    title = st.text_input("Title")
    authors = st.text_input("Authors")
    year_input = st.text_input("Year")
    journal = st.text_input("Journal")
    doi = st.text_input("DOI")
    abstract = st.text_area("Abstract")
    submitted = st.form_submit_button("Upload")

if submitted:
    if not uploaded_file or not title or not workspace:
        st.error("Workspace, title, and a PDF file are all required.")
    else:
        os.makedirs("data/uploads", exist_ok=True)
        save_path = f"data/uploads/{uploaded_file.name}"
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        text = extract_text(save_path)
        chunks = chunk_text(text)

        paper_id = insert_paper(
            title=title,
            authors=authors or None,
            year=int(year_input) if year_input.strip() else None,
            journal=journal or None,
            doi=doi or None,
            abstract=abstract or None,
            workspace=workspace,
            filename=uploaded_file.name,
            uploaded_at=datetime.datetime.now().isoformat(),
        )
        add_chunks(chunks, paper_id=paper_id, workspace=workspace)
        st.success(f"Uploaded '{title}' — split into {len(chunks)} chunks and embedded.")

st.header(f"Papers in workspace '{workspace}'")
papers = get_papers_by_workspace(workspace)
if papers:
    for paper in papers:
        st.write(f"**{paper['title']}** ({paper['year'] or 'year unknown'}) — {paper['filename']}")
else:
    st.info("No papers uploaded yet in this workspace.")

st.header("Ask a question")
query = st.text_input("Question")
if query:
    with st.spinner("Reading your papers..."):
        answer, sources = generate_answer(query, workspace=workspace)
    st.write(answer)
    if sources:
        st.caption("Sources: " + "; ".join(sources))
