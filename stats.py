from datetime import datetime
import statistics
import typing

from core import EnrichedPullRequest


class Stats(typing.TypedDict):
    mean: float
    median: float
    mode: float


def describe(pull_requests: list[EnrichedPullRequest]) -> Stats:
    lives = [
        open_for
        for pr in pull_requests
        if (open_for := pr.get("open_for")) is not None
    ]
    return dict(mean=statistics.mean(lives), median=statistics.median(lives), mode=statistics.mode(lives))
