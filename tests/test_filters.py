"""Tests for textsift.filters."""

import re

import pytest

from textsift.filters import deduplicate_lines, filter_lines, slice_lines


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
