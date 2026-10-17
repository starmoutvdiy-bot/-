"""Tests for textsift.filters."""

import re

import pytest

from textsift.filters import deduplicate_lines, filter_lines, slice_lines, transform_lines


class TestFilterLines:
    def test_basic_match(self):
        lines = ["hello world", "foo bar", "hello again"]
        assert filter_lines(lines, "hello") == ["hello world", "hello again"]

    def test_invert(self):
        lines = ["hello world", "foo bar"]
        assert filter_lines(lines, "hello", invert=True) == ["foo bar"]

    def test_ignore_case(self):
        lines = ["Hello World", "foo bar"]
        assert filter_lines(lines, "hello", ignore_case=True) == ["Hello World"]

    def test_no_matches_returns_empty(self):
        assert filter_lines(["abc", "def"], "xyz") == []

    def test_invalid_pattern_raises(self):
        with pytest.raises(re.error):
            filter_lines(["abc"], "[invalid")


class TestDeduplicateLines:
    def test_removes_duplicates(self):
        assert deduplicate_lines(["a", "b", "a", "c"]) == ["a", "b", "c"]

    def test_preserve_order(self):
        result = deduplicate_lines(["b", "a", "b"], preserve_order=True)
        assert result == ["b", "a"]

    def test_no_duplicates_unchanged(self):
        assert deduplicate_lines(["x", "y", "z"]) == ["x", "y", "z"]

    def test_empty_input(self):
        assert deduplicate_lines([]) == []


class TestSliceLines:
    lines = ["a", "b", "c", "d", "e"]

    def test_start_and_end(self):
        assert slice_lines(self.lines, 1, 3) == ["b", "c"]

    def test_defaults_return_all(self):
        assert slice_lines(self.lines) == self.lines

    def test_negative_indexing(self):
        assert slice_lines(self.lines, -2) == ["d", "e"]
        assert slice_lines(self.lines, None, -3) == ["a", "b"]

    def test_step(self):
        assert slice_lines(self.lines, step=2) == ["a", "c", "e"]

    def test_negative_step_reverses(self):
        assert slice_lines(self.lines, step=-1) == ["e", "d", "c", "b", "a"]

    def test_zero_step_raises(self):
        with pytest.raises(ValueError):
            slice_lines(self.lines, step=0)

    def test_out_of_range_is_empty(self):
        assert slice_lines(self.lines, 10, 20) == []


class TestTransformLines:
    def test_applies_in_order(self):
        result = transform_lines(["  hi  "], [str.strip, str.upper, lambda s: s + "!"])
        assert result == ["HI!"]

    def test_no_transformations_returns_input(self):
        assert transform_lines(["a", "b"], []) == ["a", "b"]

    def test_none_drops_line(self):
        drop_empty = lambda s: s or None
        assert transform_lines(["a", "  ", "b"], [str.strip, drop_empty]) == ["a", "b"]

    def test_short_circuits_after_none(self):
        calls = []

        def record(s):
            calls.append(s)
            return s

        transform_lines(["skip", "keep"], [lambda s: None if s == "skip" else s, record])
        assert calls == ["keep"]

    def test_empty_input(self):
        assert transform_lines([], [str.upper]) == []
