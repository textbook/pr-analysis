#!/usr/bin/env python3
import argparse
import datetime
import sys

from core import get_merged_pull_requests
from stats import describe


def get_options(args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--created-after", default=None, help="Filter by creation date", type=_valid_date)
    parser.add_argument("--limit", default=None, help="Number of PRs to analyse", type=int)
    parser.add_argument("--merged-before", default=None, help="Filter by merge date", type=_valid_date)
    parser.add_argument("--owner", help="Org or user", required=True, type=str)
    parser.add_argument("--repo", help="Repository", required=True, type=str)
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
    print(describe(pull_requests))
