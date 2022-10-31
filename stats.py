from datetime import datetime
import statistics
import typing

from core import PullRequest


class Stats(typing.TypedDict):
    mean: float
    median: float
    mode: float


def describe(pull_requests: list[PullRequest]) -> Stats:
    lives = [_open_for(pr) for pr in pull_requests]
    return dict(
        mean=statistics.mean(lives),
        median=statistics.median(lives),
        mode=statistics.mode(lives),
    )


def _open_for(pull_request: PullRequest) -> int:
    """Time PR was open, in hours."""
    iso_format = "%Y-%m-%dT%H:%M:%SZ"
    created = datetime.strptime(pull_request["created_at"], iso_format)
    closed = datetime.strptime(pull_request["closed_at"], iso_format)
    return round((closed - created).total_seconds() / (60 * 60))
