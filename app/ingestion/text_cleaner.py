"""Cleans messy PDF-extracted text into well-structured Markdown using
Claude, so real paragraph/section boundaries exist for chunking to use.
Raw pypdf output has no reliable paragraph signal (see docs/decisions.md) —
every line break looks the same whether it's a real paragraph break, a
mid-sentence wrap, or a header/footer that bled into the body text.
"""

from concurrent.futures import ThreadPoolExecutor

import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are cleaning up raw text extracted from an academic \
PDF. The extraction process lost paragraph structure and sometimes mixed in \
running headers/footers or interrupted a paragraph with metadata blocks.

Rewrite the text as clean Markdown:
- Reconstruct real paragraph breaks (blank line between paragraphs).
- Remove repeated running headers/footers (journal name, page numbers, \
volume/issue info that repeats).
- Remove author/correspondence blocks that interrupt body text.
- Fix obvious character-spacing artifacts from broken font encoding \
(e.g. "fu r t h er" -> "further"), only when you're confident of the \
intended word.
- Do not summarize, shorten, or paraphrase. Every sentence of real body \
content must be preserved, just cleaned up structurally.
- Output only the cleaned text — no commentary of your own."""

BATCH_SIZE = 20000  # characters of raw text sent per Claude call
MAX_WORKERS = 5  # how many batches to clean at the same time


def _clean_batch(batch):
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=8000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": batch}],
    )
    return next(block.text for block in response.content if block.type == "text")


def _split_into_batches(text, batch_size):
    return [text[i:i + batch_size] for i in range(0, len(text), batch_size)]


def clean_to_markdown(raw_text):
    batches = _split_into_batches(raw_text, BATCH_SIZE)
    print(f"Cleaning {len(batches)} batch(es), up to {MAX_WORKERS} at a time...", flush=True)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        cleaned_batches = list(executor.map(_clean_batch, batches))

    return "\n\n".join(cleaned_batches)


if __name__ == "__main__":
    from app.ingestion.pdf_extractor import extract_text

    text = extract_text("data/sample.pdf")
    cleaned = clean_to_markdown(text)
    print(f"Raw: {len(text)} chars -> Cleaned: {len(cleaned)} chars")
    print(cleaned[:1000])
