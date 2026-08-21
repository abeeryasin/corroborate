"""Step 6, the centerpiece: retrieve relevant chunks and ask Claude to answer
using only them, citing which paper each fact came from.
"""

import datetime
import time

import anthropic
from dotenv import load_dotenv

from app.db.queries import get_paper_by_id, log_question
from app.rag.vector_store import search

load_dotenv()

client = anthropic.Anthropic()

SYSTEM_PROMPT = """Answer the question using only the excerpts provided below. \
Do not use any outside knowledge, even if you know the answer some other way. \
Each excerpt is labeled with the paper it came from — when you use an excerpt, \
cite that paper. Be precise. If the excerpts don't contain enough information \
to answer the question, say "I don't know based on the uploaded papers" instead \
of guessing."""


def generate_answer(question, workspace, n_results=5):
    start_time = time.time()
    was_error = False
    answer = None
    sources = []

    try:
        results = search(question, workspace, n_results=n_results)
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        if not documents:
            answer = "No papers have been uploaded to this workspace yet."
        else:
            excerpts = []
            citations = {}
            for doc, meta in zip(documents, metadatas):
                paper = get_paper_by_id(meta["paper_id"])
                citation = f"{paper['title']} — {paper['authors'] or 'unknown authors'} ({paper['year'] or 'n.d.'})"
                citations[meta["paper_id"]] = citation
                excerpts.append(f'From "{citation}":\n{doc}')

            context = "\n\n---\n\n".join(excerpts)
            user_message = f"Excerpts:\n\n{context}\n\nQuestion: {question}"

            response = client.messages.create(
                model="claude-opus-4-8",
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_message}],
            )

            answer = next(block.text for block in response.content if block.type == "text")
            sources = list(citations.values())
    except Exception:
        was_error = True
        answer = "Something went wrong answering this question. Please try again."
    finally:
        elapsed = time.time() - start_time
        was_dont_know = "I don't know" in answer
        log_question(
            workspace=workspace,
            question=question,
            response_time_seconds=elapsed,
            was_error=was_error,
            was_dont_know=was_dont_know,
            asked_at=datetime.datetime.now().isoformat(),
        )

    return answer, sources


if __name__ == "__main__":
    answer, sources = generate_answer("mosquito breeding and rainfall", workspace="abeer-test")
    print(answer)
    print("Sources:", sources)
