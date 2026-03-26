"""Tests for textsift.filters."""

import re

import pytest

from textsift.filters import deduplicate_lines, filter_lines


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
