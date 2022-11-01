import datetime

from api import merged_pull_requests, PullRequest


def get_merged_pull_requests(
    *,
    created_after: datetime.datetime | None,
    limit: int | None,
    merged_before: datetime.datetime | None,
    owner: str,
    repo: str,
    **_,
) -> list[PullRequest]:
    """Get a list of relevant merged Pull Requests in the specified repo."""
    pull_requests = []
    for pull_request in merged_pull_requests(owner=owner, repo=repo):
        if created_after is not None and pull_request["created_at"] < _isoformat(created_after):
            break
        if merged_before is None or pull_request["merged_at"] < _isoformat(merged_before):
            pull_requests.append(pull_request)
        if limit is not None and len(pull_requests) == limit:
            break
    return pull_requests


def _isoformat(dt: datetime.datetime) -> str:
    return f"{dt.isoformat(timespec='milliseconds')}Z"
