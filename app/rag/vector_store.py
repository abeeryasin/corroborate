"""Embeds paper chunks and stores/searches them in Chroma."""

import chromadb
from sentence_transformers import SentenceTransformer

DB_PATH = "data/chroma"

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection("paper_chunks")


def add_chunks(chunks, paper_id, workspace):
    embeddings = model.encode(chunks).tolist()

    ids = []
    for i in range(len(chunks)):
        ids.append(f"{paper_id}-{i}")

    metadatas = []
    for chunk in chunks:
        metadatas.append({"workspace": workspace, "paper_id": paper_id})

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas,
    )


def delete_paper_chunks(paper_id):
    collection.delete(where={"paper_id": paper_id})


def search(query, workspace, n_results=5, max_per_paper=2):
    query_embedding = model.encode(query).tolist()
    pool_size = n_results * 4

    raw = collection.query(
        query_embeddings=[query_embedding],
        n_results=pool_size,
        where={"workspace": workspace},
    )

    documents, metadatas, ids = raw["documents"][0], raw["metadatas"][0], raw["ids"][0]

    selected_docs, selected_metas, selected_ids = [], [], []
    per_paper_count = {}
    for doc, meta, id_ in zip(documents, metadatas, ids):
        if len(selected_docs) >= n_results:
            break
        paper_id = meta["paper_id"]
        if per_paper_count.get(paper_id, 0) >= max_per_paper:
            continue
        selected_docs.append(doc)
        selected_metas.append(meta)
        selected_ids.append(id_)
        per_paper_count[paper_id] = per_paper_count.get(paper_id, 0) + 1

    return {"documents": [selected_docs], "metadatas": [selected_metas], "ids": [selected_ids]}


if __name__ == "__main__":
    from app.ingestion.pdf_extractor import extract_text
    from app.rag.chunking import chunk_text

    text = extract_text("data/sample.pdf")
    chunks = chunk_text(text)
    add_chunks(chunks, paper_id=1, workspace="abeer-test")

    results = search("mosquito breeding and rainfall", workspace="abeer-test")
    print(results["documents"])
