import datetime

from api import merged_pull_requests, PullRequest


class EnrichedPullRequest(PullRequest):
    open_for: int


def get_merged_pull_requests(
    *,
    created_after: datetime.datetime | None,
    limit: int | None,
    merged_before: datetime.datetime | None,
    owner: str,
    repo: str,
    **_,
) -> list[EnrichedPullRequest]:
    """Get a list of relevant merged Pull Requests in the specified repo."""
    pull_requests = []
    for pull_request in merged_pull_requests(owner=owner, repo=repo):
        if created_after is not None and pull_request["created_at"] < _isoformat(created_after):
            break
        if merged_before is None or pull_request["merged_at"] < _isoformat(merged_before):
            pull_requests.append(dict(open_for=_open_for(pull_request), **pull_request))
        if limit is not None and len(pull_requests) == limit:
            break
    return pull_requests


def _isoformat(dt: datetime.datetime) -> str:
    return f"{dt.isoformat(timespec='milliseconds')}Z"


def _open_for(pull_request: PullRequest) -> int:
    """Time PR was open, in hours."""
    iso_format = "%Y-%m-%dT%H:%M:%SZ"
    created = datetime.datetime.strptime(pull_request["created_at"], iso_format)
    closed = datetime.datetime.strptime(pull_request["closed_at"], iso_format)
    return round((closed - created).total_seconds() / (60 * 60))
