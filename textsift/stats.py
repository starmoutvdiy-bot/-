"""Text statistics and summarization functions for textsift."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field


@dataclass
class TextStats:
    """Aggregate statistics for a body of text."""

    line_count: int = 0
    word_count: int = 0
    char_count: int = 0
    unique_words: int = 0
    top_words: list[tuple[str, int]] = field(default_factory=list)


def compute_stats(lines: list[str], *, top_n: int = 10) -> TextStats:
    """Compute aggregate statistics over a list of text lines.

    Args:
        lines: Input lines of text.
        top_n: How many of the most frequent words to include.

    Returns:
        A populated TextStats instance.
    """
    word_counter: Counter[str] = Counter()

    for line in lines:
        words = line.lower().split()
        word_counter.update(words)

    return TextStats(
        line_count=len(lines),
        word_count=sum(word_counter.values()),
        char_count=sum(len(line) for line in lines),
        unique_words=len(word_counter),
        top_words=word_counter.most_common(top_n),
    )


def format_stats(stats: TextStats) -> str:
    """Return a human-readable summary of a TextStats object.

    Args:
        stats: A populated TextStats instance.

    Returns:
        A multi-line formatted string with right-aligned, comma-separated counts
        and a top-words list in the form word(count), ...
    """
    top = ", ".join(f"{word}({count:,})" for word, count in stats.top_words)
    return (
        f"Lines  : {stats.line_count:>9,}\n"
        f"Words  : {stats.word_count:>9,}\n"
        f"Chars  : {stats.char_count:>9,}\n"
        f"Unique : {stats.unique_words:>9,}\n"
        f"Top words: {top}"
    )


_VOWEL_GROUP = re.compile(r"[aeiouy]+")
_SENTENCE_END = re.compile(r"[.!?]+")
_WORD = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")


def count_syllables(word: str) -> int:
    """Estimate the number of syllables in a word using vowel groups.

    Each run of consecutive vowels counts as one syllable. A trailing silent
    "e" is not counted (except in "-le" endings such as "table"). Every word
    has at least one syllable.
    """
    word = word.lower()
    count = len(_VOWEL_GROUP.findall(word))
    if word.endswith("e") and not word.endswith("le") and count > 1:
        count -= 1
    return max(count, 1)


def compute_readability(lines: list[str]) -> float:
    """Return the Flesch reading ease score for a body of text.

    Uses the Flesch (1948) formula:

        206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)

    Higher scores mean easier text (roughly 0-100 for typical prose).
    Syllables are estimated heuristically, so the score is approximate.

    Args:
        lines: Input lines of text.

    Returns:
        The reading ease score, or 0.0 if the text contains no words.
    """
    text = " ".join(lines)
    words = _WORD.findall(text)
    if not words:
        return 0.0
    sentences = max(len(_SENTENCE_END.findall(text)), 1)
    syllables = sum(count_syllables(word) for word in words)
    return (
        206.835
        - 1.015 * (len(words) / sentences)
        - 84.6 * (syllables / len(words))
    )
