"""Text statistics and summarization functions for textsift."""

from __future__ import annotations

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


# TODO (medium): Add a `compute_readability(lines)` function that returns a
# Flesch-Kincaid reading ease score. Requires counting syllables per word
# (a heuristic approach using vowel groups is acceptable). Add a brief
# docstring citing the formula.
