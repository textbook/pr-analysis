import os
import textwrap
import typing

import requests


STATE = typing.Literal["CLOSED", "OPEN", "MERGED"]


class PullRequest(typing.TypedDict):
    closed_at: str | None
    created_at: str
    id: str
    labels: list[str]
    merged_at: str | None
    number: int
    title: str


def fetch_pull_requests(
    *,
    closed: bool,
    merged: bool,
    owner: str,
    repo: str,
) -> typing.Iterable[PullRequest]:
    states: list[STATE] = []
    if closed:
        states.append("CLOSED")
    if merged:
        states.append("MERGED")
    headers = dict(Authorization=f"Bearer {os.environ['GITHUB_PAT']}")
    response = requests.post(
        "https://api.github.com/graphql",
        headers=headers,
        json=dict(query=_query(owner, repo, states)),
    )
    response.raise_for_status()
    pull_requests = response.json()["data"]["repository"]["pullRequests"]
    yield from map(_normalise_edge, pull_requests["edges"])
    while (page_info := pull_requests["pageInfo"])["hasNextPage"]:
        response = requests.post(
            "https://api.github.com/graphql",
            headers=headers,
            json=dict(query=_query(owner, repo, states, page_info["endCursor"])),
        )
        response.raise_for_status()
        pull_requests = response.json()["data"]["repository"]["pullRequests"]
        yield from map(_normalise_edge, pull_requests["edges"])


def _query(owner: str, repo: str, states: list[STATE], cursor: str = None) -> str:
    return textwrap.dedent(f"""
        query {{
            repository(owner: "{owner}", name: "{repo}") {{
                pullRequests(
                    {"" if cursor is None else f'after: "{cursor}",'}
                    first: 100,
                    orderBy: {{field: CREATED_AT, direction: DESC}},
                    {f'states: [{", ".join(states)}],' if states else ""}
                ) {{
                    edges {{
                        node {{
                            closedAt
                            createdAt
                            id
                            labels (first: 100) {{
                                edges {{
                                    node {{
                                        name
                                    }}
                                }}
                            }}
                            mergedAt
                            number
                            title
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
    node = edge["node"]
    labels = [
        label["node"]["name"]
        for label in node["labels"]["edges"]
    ]
    normalised = {
        KEY_MAP.get(key, key): value
        for key, value in node.items()
        if key not in ("labels",)
    }
    return dict(**normalised, labels=labels)
