"""Text filtering functions for textsift."""

from __future__ import annotations

import re


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


# TODO (medium): Add a `slice_lines(lines, start, end)` function that supports
# Python-style negative indexing and step values, mirroring the semantics of
# list slicing. Should raise ValueError for invalid step=0. Add corresponding
# tests in tests/test_filters.py.


# TODO (hard): Add a `transform_lines(lines, transformations)` function where
# `transformations` is a list of callables applied in sequence to each line.
# Should support short-circuit: if a transformation returns None, skip that
# line entirely. This would allow composable pipelines (strip, upper, filter).
