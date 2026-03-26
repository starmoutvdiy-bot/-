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


# TODO (straightforward): Implement `format_stats(stats: TextStats) -> str` that
# returns a human-readable multi-line string summary of a TextStats object.
# Example output:
#
#   Lines  :     142
#   Words  :   1,203
#   Chars  :   7,840
#   Unique :     318
#   Top words: the(45), and(30), is(18), ...
#
# Use str.format or an f-string with number formatting (comma separators for
# counts). Return the string; do not print it. Add tests in test_stats.py.


# TODO (medium): Add a `compute_readability(lines)` function that returns a
# Flesch-Kincaid reading ease score. Requires counting syllables per word
# (a heuristic approach using vowel groups is acceptable). Add a brief
# docstring citing the formula.
