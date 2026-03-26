"""Tests for textsift.stats."""

from textsift.stats import TextStats, compute_stats, format_stats


class TestComputeStats:
    def test_line_and_word_counts(self):
        lines = ["hello world", "foo bar baz"]
        stats = compute_stats(lines)
        assert stats.line_count == 2
        assert stats.word_count == 5

    def test_char_count(self):
        stats = compute_stats(["abc", "de"])
        assert stats.char_count == 5  # 3 + 2

    def test_unique_words(self):
        stats = compute_stats(["the cat sat", "the cat"])
        assert stats.unique_words == 3  # "the", "cat", "sat"

    def test_top_words_ordering(self):
        stats = compute_stats(["a a a b b c"], top_n=2)
        assert stats.top_words[0] == ("a", 3)
        assert stats.top_words[1] == ("b", 2)

    def test_empty_input(self):
        stats = compute_stats([])
        assert stats.line_count == 0
        assert stats.word_count == 0
        assert stats.char_count == 0


class TestFormatStats:
    def test_contains_all_fields(self):
        stats = TextStats(
            line_count=10,
            word_count=100,
            char_count=500,
            unique_words=40,
            top_words=[("the", 15), ("and", 10)],
        )
        output = format_stats(stats)
        assert "10" in output
        assert "100" in output
        assert "500" in output
        assert "40" in output
        assert "the" in output
        assert "15" in output

    def test_returns_string(self):
        stats = TextStats()
        assert isinstance(format_stats(stats), str)

    def test_comma_formatting_for_large_numbers(self):
        stats = TextStats(line_count=1000, word_count=20000, char_count=100000, unique_words=500)
        output = format_stats(stats)
        assert "1,000" in output
        assert "20,000" in output

    def test_empty_top_words(self):
        stats = TextStats(top_words=[])
        output = format_stats(stats)
        assert "Top words" in output  # label still present even if empty
