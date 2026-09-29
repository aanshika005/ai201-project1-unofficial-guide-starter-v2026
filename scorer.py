"""
Eval scoring — does an answer contain what a correct answer has to contain?

Unit 2, second measured improvement. The original is kept below as
`judge_v1` rather than deleted, so the README can show both.

The original was a bare substring test, and it failed in two directions:

  - FALSE NEGATIVE. `expects="doesn't count"` against an answer saying "do not
    count" scored fail on all six runs, before and after, even though the
    answer was correct, grounded and cited. The document says "don't count",
    so the wording the test demanded was never going to appear.

  - FALSE POSITIVE, which is worse. `expects="W"` lowercases to "w", and every
    English sentence contains a w somewhere. That question passed
    unconditionally — it would have passed on a wrong answer too.

This version fixes the mechanism rather than the two instances: it normalises
contractions and punctuation on both sides, accepts a list of acceptable
phrasings, and refuses to score against an `expects` too short to mean
anything.
"""

import re

# Contractions that show up in this corpus, mapped to their expanded form so
# "don't count", "doesn't count" and "do not count" all compare equal.
_CONTRACTIONS = {
    "don't": "do not",
    "doesn't": "does not",
    "didn't": "did not",
    "won't": "will not",
    "can't": "cannot",
    "isn't": "is not",
    "aren't": "are not",
    "wasn't": "was not",
    "weren't": "were not",
    "it's": "it is",
    "that's": "that is",
    "you're": "you are",
    "they're": "they are",
}

MIN_PHRASE = 3   # an `expects` shorter than this matches by accident, not by meaning


def _normalise(text: str) -> str:
    """Lowercase, expand contractions, and flatten punctuation and spacing."""
    text = (text or "").lower()
    text = text.replace("’", "'")          # curly apostrophe -> straight
    for short, long in _CONTRACTIONS.items():
        text = text.replace(short, long)
    text = re.sub(r"[^a-z0-9:$.\s-]", " ", text)  # keep digits, times, prices
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def judge(question: str, expects, answer: str, results) -> bool:
    """
    True if the answer contains an acceptable phrasing of what it must contain.

    `expects` may be a single string or a list of acceptable phrasings. A
    phrase shorter than MIN_PHRASE characters after normalising is skipped —
    see the module docstring for why.
    """
    if not expects:
        return False

    candidates = [expects] if isinstance(expects, str) else list(expects)
    text = _normalise(answer)

    for phrase in candidates:
        phrase = _normalise(phrase)
        if len(phrase) < MIN_PHRASE:
            continue
        if phrase in text:
            return True
    return False


def judge_v1(question: str, expects: str, answer: str, results) -> bool:
    """The original, kept for the before/after comparison. Not called."""
    if not expects:
        return False
    return expects.strip().lower() in (answer or "").lower()
