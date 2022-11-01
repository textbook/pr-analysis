#!/usr/bin/env python3
import argparse
import csv
import datetime
import json
import sys
import typing

from core import EnrichedPullRequest, get_merged_pull_requests
from stats import describe


def get_options(args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Perform statistical analysis on merged pull requests")
    parser.add_argument("owner", help="Org or user", type=str)
    parser.add_argument("repo", help="Repository", type=str)
    parser.add_argument("--created-after", help="Filter by creation date", type=_valid_date)
    parser.add_argument("--csv", help="Save PR data to CSV file", type=argparse.FileType("w"))
    parser.add_argument("--json", help="Save PR data to JSON file", type=argparse.FileType("w"))
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


def _write_csv(pull_requests: list[EnrichedPullRequest], csv_file: typing.TextIO) -> None:
    writer = csv.DictWriter(csv_file, fieldnames=list(pull_requests[0].keys()))
    writer.writeheader()
    writer.writerows(pull_requests)
    csv_file.close()


def _write_json(pull_requests: list[EnrichedPullRequest], json_file: typing.TextIO, pretty: bool) -> None:
    json.dump(
        pull_requests,
        json_file,
        indent=2 if pretty else None,
        separators=(",", ": ") if pretty else (",", ":"),
    )
    json_file.close()


if __name__ == "__main__":
    options = get_options(sys.argv[1:])
    pull_requests = get_merged_pull_requests(**vars(options))
    print(f"analysing {len(pull_requests):,} merged PRs")
    if options.csv is not None:
        _write_csv(pull_requests, options.csv)
    if options.json is not None:
        _write_json(pull_requests, options.json, options.pretty)
    print(describe(pull_requests))
