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


def search(query, workspace, n_results=5):
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where={"workspace": workspace},
    )
    return results


if __name__ == "__main__":
    from app.ingestion.pdf_extractor import extract_text
    from app.rag.chunking import chunk_text

    text = extract_text("data/sample.pdf")
    chunks = chunk_text(text)
    add_chunks(chunks, paper_id=1, workspace="abeer-test")

    results = search("mosquito breeding and rainfall", workspace="abeer-test")
    print(results["documents"])
