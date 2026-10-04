"""Pure state transformations, separate from publication."""
from dataclasses import replace
from .models import validate_submission
from .policy import require_actor, require_version, require_state, require_owner, require_review


def check(item, actor, expected_version, state):
    require_actor(actor)
    require_version(item, expected_version)
    require_state(item, state)


def claim(item, actor, expected_version):
    check(item, actor, expected_version, "queued")
    return replace(item, state="claimed", version=item.version+1, owner=actor)


def submit(item, actor, expected_version, data):
    check(item, actor, expected_version, "claimed")
    require_owner(item, actor)
    validate_submission(data)
    return replace(item, state="submitted", version=item.version+1, submission=data)


def review(item, actor, expected_version, approved, score=None, reason=None):
    check(item, actor, expected_version, "submitted")
    require_review(item, actor, approved, score, reason)
    state = "approved"
    details = dict(reviewer=actor, score=score if approved else None, reason=None if approved else reason)
    return replace(item, state=state, version=item.version+1, review=details)


def requeue(item, actor, expected_version):
    check(item, actor, expected_version, "rejected")
    return replace(item, state="queued", version=item.version+1,
                   owner=None, submission=item.submission, review=None)


def available_actions(item):
    return {"queued": ("claim",), "claimed": ("submit",), "submitted": ("review",),
            "approved": (), "rejected": ("requeue",)}[item.state]
