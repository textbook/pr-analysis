import os
import textwrap
import typing

import requests


class PullRequest(typing.TypedDict):
    closed_at: str
    created_at: str
    id: str
    merged_at: str
    number: int


def merged_pull_requests(*, owner: str, repo: str) -> typing.Iterable[PullRequest]:
    headers = dict(Authorization=f"Bearer {os.environ['GITHUB_PAT']}")
    response = requests.post(
        "https://api.github.com/graphql",
        headers=headers,
        json=dict(query=_query(owner, repo)),
    )
    response.raise_for_status()
    pull_requests = response.json()["data"]["repository"]["pullRequests"]
    yield from map(_normalise_edge, pull_requests["edges"])
    while pull_requests["pageInfo"]["hasNextPage"]:
        response = requests.post(
            "https://api.github.com/graphql",
            headers=headers,
            json=dict(query=_query(owner, repo, pull_requests["pageInfo"]["endCursor"])),
        )
        response.raise_for_status()
        pull_requests = response.json()["data"]["repository"]["pullRequests"]
        yield from map(_normalise_edge, pull_requests["edges"])


def _query(owner: str, repo: str, cursor: str = None) -> str:
    return textwrap.dedent(f"""
        query {{
            repository(owner: "{owner}", name: "{repo}") {{
                pullRequests(
                    {"" if cursor is None else f'after: "{cursor}",'}
                    first: 100,
                    orderBy: {{field: CREATED_AT, direction: DESC}},
                    states: [MERGED]
                ) {{
                    edges {{
                        node {{
                            closedAt
                            createdAt
                            id
                            mergedAt
                            number
                        }}
                    }}
                    pageInfo {{
                        endCursor
                        hasNextPage
                    }}
                }}
            }}
        }}
    """)


KEY_MAP = dict(createdAt="created_at", closedAt="closed_at", mergedAt="merged_at")


def _normalise_edge(edge: dict[str, dict[str, str]]) -> dict[str, str]:
    return {KEY_MAP.get(key, key): value for key, value in edge["node"].items()}
