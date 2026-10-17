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


def count_syllables(word: str) -> int:
    """Estimate the number of syllables in a word using vowel groups.

    A trailing silent "e" is not counted, and every word has at least one
    syllable.
    """
    word = re.sub(r"[^a-z]", "", word.lower())
    if not word:
        return 0
    groups = re.findall(r"[aeiouy]+", word)
    count = len(groups)
    if word.endswith("e") and not word.endswith("le") and count > 1:
        count -= 1
    return max(count, 1)


def compute_readability(lines: list[str]) -> float:
    """Return the Flesch reading ease score for the given lines.

    Uses the formula:
        206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)

    Higher scores mean easier text. Sentences are counted by runs of ".",
    "!" or "?" (at least one sentence when there is any text). Returns 0.0
    when there are no words.
    """
    text = " ".join(lines)
    words = [w for w in text.split() if re.search(r"[A-Za-z]", w)]
    if not words:
        return 0.0
    sentences = max(len(re.findall(r"[.!?]+", text)), 1)
    syllables = sum(count_syllables(w) for w in words)
    return 206.835 - 1.015 * (len(words) / sentences) - 84.6 * (syllables / len(words))
