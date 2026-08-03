"""Ask Claude to read a paper's first page and extract its bibliographic
metadata (title, authors, year, journal, DOI, abstract), so the user
doesn't have to type it in by hand.
"""

import json

import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are extracting bibliographic metadata from the \
beginning of an academic paper. Use only what's actually printed in the \
text below — never guess or invent a value. If a field genuinely isn't \
present, return an empty string for it."""


def extract_metadata(text):
    first_page = text[:3000]

    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": first_page}],
        output_config={
            "format": {
                "type": "json_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "authors": {"type": "string"},
                        "year": {"type": "string"},
                        "journal": {"type": "string"},
                        "doi": {"type": "string"},
                        "abstract": {"type": "string"},
                    },
                    "required": ["title", "authors", "year", "journal", "doi", "abstract"],
                    "additionalProperties": False,
                },
            }
        },
    )

    text_block = next(block.text for block in response.content if block.type == "text")
    return json.loads(text_block)


if __name__ == "__main__":
    from app.ingestion.pdf_extractor import extract_text

    text = extract_text("data/sample.pdf")
    metadata = extract_metadata(text)
    print(metadata)
