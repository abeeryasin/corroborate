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
from app.db.queries import insert_paper, get_papers_by_workspace, get_all_workspaces, delete_paper
from app.ingestion.pdf_extractor import extract_text
from app.ingestion.metadata_extractor import extract_metadata
from app.rag.chunking import chunk_text
from app.rag.vector_store import add_chunks, delete_paper_chunks
from app.rag.generation import generate_answer

init_db()

st.title("Corroborate")
st.caption("Upload research papers, ask questions, get answers cited back to the source.")

existing_workspaces = get_all_workspaces()
NEW_WORKSPACE_LABEL = "Add new workspace"

selected_workspace = st.selectbox("Workspace", existing_workspaces + [NEW_WORKSPACE_LABEL])

if selected_workspace == NEW_WORKSPACE_LABEL:
    workspace = st.text_input("New workspace name")
else:
    workspace = selected_workspace

with st.expander("Upload a paper", expanded=False):
    uploaded_file = st.file_uploader("PDF file", type="pdf")

    extracted = {"title": "", "authors": "", "year": "", "journal": "", "doi": "", "abstract": ""}
    raw_text = ""

    if uploaded_file is not None:
        if st.session_state.get("last_uploaded_name") != uploaded_file.name:
            os.makedirs("data/uploads", exist_ok=True)
            save_path = f"data/uploads/{uploaded_file.name}"
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner("Reading the PDF and detecting title/authors/year..."):
                raw_text = extract_text(save_path)
                extracted = extract_metadata(raw_text)

            st.session_state["last_uploaded_name"] = uploaded_file.name
            st.session_state["last_uploaded_text"] = raw_text
            st.session_state["extracted_metadata"] = extracted
        else:
            raw_text = st.session_state.get("last_uploaded_text", "")
            extracted = st.session_state.get("extracted_metadata", extracted)

        st.caption("Fields below were auto-detected from the PDF — review and fix anything wrong before uploading.")

    with st.form("upload_form", clear_on_submit=True):
        title = st.text_input("Title", value=extracted["title"])
        authors = st.text_input("Authors", value=extracted["authors"])
        year_input = st.text_input("Year", value=extracted["year"])
        journal = st.text_input("Journal", value=extracted["journal"])
        doi = st.text_input("DOI", value=extracted["doi"])
        abstract = st.text_area("Abstract", value=extracted["abstract"])
        submitted = st.form_submit_button("Upload")

    if submitted:
        if not uploaded_file or not title or not workspace:
            st.error("Workspace, title, and a PDF file are all required.")
        else:
            text = raw_text or extract_text(f"data/uploads/{uploaded_file.name}")
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

if workspace:
    st.header(f"Papers in workspace '{workspace}'")
    papers = get_papers_by_workspace(workspace)
    if papers:
        for paper in papers:
            st.write(f"**{paper['title']}** ({paper['year'] or 'year unknown'}) — {paper['filename']}")

            confirm_key = f"confirm_delete_{paper['id']}"

            if st.session_state.get(confirm_key):
                st.warning(f"Delete '{paper['title']}'? This can't be undone.")
                if st.button("Yes, delete it", key=f"yes_{paper['id']}"):
                    delete_paper(paper['id'])
                    delete_paper_chunks(paper['id'])
                    del st.session_state[confirm_key]
                    st.rerun()
                if st.button("Cancel", key=f"cancel_{paper['id']}"):
                    del st.session_state[confirm_key]
                    st.rerun()
            else:
                if st.button("Delete", key=f"delete_{paper['id']}"):
                    st.session_state[confirm_key] = True
                    st.rerun()
    else:
        st.info("No papers uploaded yet in this workspace.")

st.header("Ask a question")
query = st.text_input("Question")

if query and query != st.session_state.get("last_answered_question"):
    with st.spinner("Reading your papers..."):
        answer, sources = generate_answer(query, workspace=workspace)
    st.write(answer)
    if sources:
        st.caption("Sources: " + "; ".join(sources))

    st.session_state.setdefault("qa_history", []).append(
        {"question": query, "answer": answer, "sources": sources}
    )
    st.session_state["last_answered_question"] = query

if len(st.session_state.get("qa_history", [])) > 1:
    st.subheader("Previously asked questions")
    prior_qa = list(reversed(st.session_state["qa_history"][:-1]))
    qa_by_question = {qa["question"]: qa for qa in prior_qa}
    selected_question = st.selectbox("Select a previous question", qa_by_question.keys())
    selected_qa = qa_by_question[selected_question]
    st.write(selected_qa["answer"])
    if selected_qa["sources"]:
        st.caption("Sources: " + "; ".join(selected_qa["sources"]))
