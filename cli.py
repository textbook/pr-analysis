#!/usr/bin/env python3
import argparse
import sys

from core import get_closed_pull_requests
from stats import describe


def get_options(args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", help="Org or user", required=True, type=str)
    parser.add_argument("--repo", help="Repository", required=True, type=str)
    parser.add_argument("--limit", default=None, help="Max PRs to fetch", type=int)
    return parser.parse_args(args)


if __name__ == "__main__":
    options = get_options(sys.argv[1:])
    pull_requests = get_closed_pull_requests(
        limit=options.limit,
        owner=options.owner,
        repo=options.repo,
    )
    print(f"analysing {len(pull_requests):,} closed PRs")
    print(describe(pull_requests))
