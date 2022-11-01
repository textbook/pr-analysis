import datetime
import os
import typing

import requests


class PullRequest(typing.TypedDict):
    created_at: str
    closed_at: str
    merged_at: str
    state: typing.Literal["open", "closed"]


def closed_pull_requests(*, owner: str, repo: str) -> typing.Iterable[PullRequest]:
    headers = dict(
        Accept="application/vnd.github+json",
        Authorization=f"Bearer {os.environ['GITHUB_PAT']}",
    )
    response = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/pulls",
        headers=headers,
        params=dict(per_page="100", state="closed"),
    )
    response.raise_for_status()
    yield from response.json()
    while (next_page := _get_next_page(response.headers["Link"])) is not None:
        response = requests.get(next_page, headers=headers)
        response.raise_for_status()
        yield from response.json()


def get_merged_pull_requests(
    *,
    created_after: datetime.datetime | None,
    limit: int | None,
    merged_before: datetime.datetime | None,
    owner: str,
    repo: str,
) -> list[PullRequest]:
    """Get a list of all merged Pull Requests in the specified repo."""
    pull_requests = []
    for pull_request in closed_pull_requests(owner=owner, repo=repo):
        if created_after is not None and pull_request["created_at"] < _isoformat(created_after):
            break
        if (
            (merged_at := pull_request["merged_at"]) is not None
            and (merged_before is None or merged_at < _isoformat(merged_before))
        ):
            pull_requests.append(pull_request)
        if limit is not None and len(pull_requests) == limit:
            break
    return pull_requests


def _get_next_page(header: str) -> str | None:
    """Get the URL of the next page."""
    links = {
        rel[5:-1]: url[1:-1]
        for url, rel in (
            link.split("; ") for link in header.split(", ")
        )
    }
    return links.get("next")


def _isoformat(dt: datetime.datetime) -> str:
    return f"{dt.isoformat(timespec='milliseconds')}Z"
