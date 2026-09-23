"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def _blocks(text: str) -> list[str]:
    """Blank-line-separated paragraphs, empties dropped."""
    return [b.strip() for b in text.strip().split("\n\n") if b.strip()]


def _looks_like_title(block: str) -> bool:
    """A campus_life document opens with a short one-line heading."""
    return "\n" not in block and len(block) < 120


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Paragraph-aware chunker for campus_life.

    The corpus is 88 short posts averaging 317 characters, and most of them are
    already a single thought — splitting those would only manufacture
    fragments. A handful are not: the longest, housing_old_brewhouse.txt, packs
    brewery history, heating, laundry prices and noise into 554 characters, so
    a question about any one of those matches a vector that is mostly about the
    other three.

    So the strategy is conditional. A document is left whole unless it is both
    longer than config.SPLIT_ABOVE and carries at least
    config.MIN_BODY_PARAGRAPHS body paragraphs. When a document does split, it
    splits on paragraph boundaries rather than a character count, short
    paragraphs are merged forward until they clear config.MIN_CHUNK, and the
    document's title line is prepended to every piece — without it, "The bad:
    the heating is uneven" no longer says which building it is about.

    No character overlap: paragraph boundaries do not sever sentences, and the
    repeated title already carries the shared context that overlap exists for.
    """
    chunks: list[Chunk] = []

    for doc in documents:
        blocks = _blocks(doc.text)
        if not blocks:
            continue

        has_title = len(blocks) > 1 and _looks_like_title(blocks[0])
        title = blocks[0] if has_title else ""
        body = blocks[1:] if has_title else blocks

        # Leave short or single-topic posts exactly as they are.
        if len(doc.text) <= config.SPLIT_ABOVE or len(body) < config.MIN_BODY_PARAGRAPHS:
            pieces = [doc.text.strip()]
        else:
            # Merge paragraphs forward until each piece clears the floor.
            merged: list[str] = []
            buffer = ""
            for para in body:
                buffer = f"{buffer}\n\n{para}" if buffer else para
                if len(buffer) >= config.MIN_CHUNK:
                    merged.append(buffer)
                    buffer = ""
            if buffer:                       # trailing remainder is never left alone
                if merged:
                    merged[-1] = f"{merged[-1]}\n\n{buffer}"
                else:
                    merged.append(buffer)

            pieces = [f"{title}\n\n{m}" if title else m for m in merged]

        for index, piece in enumerate(pieces):
            chunks.append(
                Chunk(
                    text=piece,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
