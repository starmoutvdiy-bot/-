"""Command-line interface for textsift."""

from __future__ import annotations

import click

from textsift.filters import deduplicate_lines, filter_lines
from textsift.stats import TextStats, compute_stats, format_stats


@click.group()
@click.version_option()
def main() -> None:
    """textsift - filter and summarize text from files or stdin."""


@main.command("filter")
@click.argument("file", type=click.File("r"), default="-")
@click.option("-p", "--pattern", required=True, help="Regex pattern to match.")
@click.option("-v", "--invert", is_flag=True, default=False, help="Invert match.")
@click.option("-i", "--ignore-case", is_flag=True, default=False)
def filter_cmd(file: click.File, pattern: str, invert: bool, ignore_case: bool) -> None:
    """Filter lines from FILE (or stdin) by PATTERN."""
    lines = file.readlines()
    stripped = [line.rstrip("\n") for line in lines]
    results = filter_lines(stripped, pattern, invert=invert, ignore_case=ignore_case)
    for line in results:
        click.echo(line)


@main.command("dedup")
@click.argument("file", type=click.File("r"), default="-")
@click.option("--no-preserve-order", is_flag=True, default=False)
def dedup_cmd(file: click.File, no_preserve_order: bool) -> None:
    """Remove duplicate lines from FILE (or stdin)."""
    lines = [line.rstrip("\n") for line in file.readlines()]
    results = deduplicate_lines(lines, preserve_order=not no_preserve_order)
    for line in results:
        click.echo(line)


@main.command("stats")
@click.argument("file", type=click.File("r"), default="-")
@click.option("--top-n", default=10, show_default=True, help="Number of top words.")
def stats_cmd(file: click.File, top_n: int) -> None:
    """Print statistics for FILE (or stdin)."""
    lines = [line.rstrip("\n") for line in file.readlines()]
    stats = compute_stats(lines, top_n=top_n)
    click.echo(format_stats(stats))
