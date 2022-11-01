#!/usr/bin/env python3
import argparse
import sys

from core import get_merged_pull_requests
from stats import describe


def get_options(args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", help="Org or user", required=True, type=str)
    parser.add_argument("--repo", help="Repository", required=True, type=str)
    parser.add_argument("--limit", default=None, help="Number of PRs to analyse", type=int)
    return parser.parse_args(args)


if __name__ == "__main__":
    options = get_options(sys.argv[1:])
    pull_requests = get_merged_pull_requests(**vars(options))
    print(f"analysing {len(pull_requests):,} merged PRs")
    print(describe(pull_requests))
