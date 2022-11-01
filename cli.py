#!/usr/bin/env python3
import argparse
import datetime
import json
import sys

from core import get_merged_pull_requests
from stats import describe


def get_options(args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Perform statistical analysis on merged pull requests")
    parser.add_argument("owner", help="Org or user", type=str)
    parser.add_argument("repo", help="Repository", type=str)
    parser.add_argument("--created-after", help="Filter by creation date", type=_valid_date)
    parser.add_argument("--json", help="Save PR data to file", type=argparse.FileType("w"))
    parser.add_argument("--limit", help="Number of PRs to analyse", type=int)
    parser.add_argument("--merged-before", help="Filter by merge date", type=_valid_date)
    parser.add_argument("--pretty", action="store_true", help="Human-readable JSON")
    return parser.parse_args(args)


def _valid_date(value: str) -> datetime.datetime:
    try:
        return datetime.datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        msg = "not a valid date: {0!r}".format(value)
        raise argparse.ArgumentTypeError(msg)


if __name__ == "__main__":
    options = get_options(sys.argv[1:])
    pull_requests = get_merged_pull_requests(**vars(options))
    print(f"analysing {len(pull_requests):,} merged PRs")
    if options.json:
        json.dump(
            pull_requests,
            options.json,
            indent=2 if options.pretty else None,
            separators=(",", ": ") if options.pretty else (",", ":"),
        )
    print(describe(pull_requests))
