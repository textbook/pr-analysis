from datetime import datetime
import statistics
import typing

from core import EnrichedPullRequest


class Stats(typing.TypedDict):
    mean: float
    median: float
    mode: float


def describe(pull_requests: list[EnrichedPullRequest]) -> Stats:
    lives = [pr["open_for"] for pr in pull_requests]
    return dict(mean=statistics.mean(lives), median=statistics.median(lives), mode=statistics.mode(lives))
