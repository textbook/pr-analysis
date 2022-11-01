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
    at_least: int | None,
    owner: str,
    repo: str,
) -> list[PullRequest]:
    """Get a list of all merged Pull Requests in the specified repo."""
    pull_requests = []
    for pull_request in closed_pull_requests(owner=owner, repo=repo):
        if pull_request["merged_at"] is not None:
            pull_requests.append(pull_request)
        if at_least is not None and len(pull_requests) == at_least:
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
