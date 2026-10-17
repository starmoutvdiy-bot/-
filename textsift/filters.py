"""Text filtering functions for textsift."""

from __future__ import annotations

import re
from collections.abc import Callable


def filter_lines(
    lines: list[str],
    pattern: str,
    *,
    invert: bool = False,
    ignore_case: bool = False,
) -> list[str]:
    """Return lines that match (or do not match) a regex pattern.

    Args:
        lines: Input lines to filter.
        pattern: Regular expression pattern to match against.
        invert: If True, return lines that do NOT match.
        ignore_case: If True, perform case-insensitive matching.

    Returns:
        Filtered list of lines.
    """
    flags = re.IGNORECASE if ignore_case else 0
    compiled = re.compile(pattern, flags)
    match_fn = compiled.search

    if invert:
        return [line for line in lines if not match_fn(line)]
    return [line for line in lines if match_fn(line)]


def deduplicate_lines(lines: list[str], *, preserve_order: bool = True) -> list[str]:
    """Return lines with duplicates removed.

    Args:
        lines: Input lines.
        preserve_order: If True, maintain original order of first occurrences.
            If False, the result order is undefined (faster for large inputs).

    Returns:
        Lines with duplicates removed.
    """
    if preserve_order:
        seen: set[str] = set()
        result = []
        for line in lines:
            if line not in seen:
                seen.add(line)
                result.append(line)
        return result
    return list(set(lines))


def slice_lines(
    lines: list[str],
    start: int | None = None,
    end: int | None = None,
    step: int | None = None,
) -> list[str]:
    """Return a slice of lines using Python list slicing semantics.

    Args:
        lines: Input lines.
        start: Start index (inclusive). Negative values count from the end.
        end: End index (exclusive). Negative values count from the end.
        step: Step between lines. Negative values reverse the direction.

    Returns:
        The sliced list of lines.

    Raises:
        ValueError: If step is 0.
    """
    if step == 0:
        raise ValueError("step must not be zero")
    return lines[start:end:step]


def transform_lines(
    lines: list[str],
    transformations: list[Callable[[str], str | None]],
) -> list[str]:
    """Apply a sequence of transformations to each line.

    Each transformation receives the output of the previous one. If any
    transformation returns None, the line is dropped and the remaining
    transformations are skipped for it.

    Args:
        lines: Input lines.
        transformations: Callables applied in order to each line.

    Returns:
        The transformed lines, excluding any that were dropped.
    """
    result = []
    for line in lines:
        current: str | None = line
        for transform in transformations:
            current = transform(current)
            if current is None:
                break
        if current is not None:
            result.append(current)
    return result
