"""Version, actor and state checks at transition boundaries."""
import math


class TransitionError(ValueError):
    pass


class VersionConflict(TransitionError):
    pass


def require_actor(actor):
    if not isinstance(actor, str) or not actor.strip():
        raise TransitionError("Actor is required")


def require_version(item, expected_version):
    if item.version != expected_version:
        raise VersionConflict("Stale task version")


def require_state(item, state):
    if item.state != state:
        raise TransitionError("Transition unavailable from " + item.state)


def require_owner(item, actor):
    if item.id != actor:
        raise TransitionError("Only the owner may submit")


def require_review(item, actor, approved, score, reason):
    if item.owner == actor:
        raise TransitionError("Owner cannot review own work")
    if approved:
        if score is None or not math.isfinite(score) or not 0 <= score <= 1:
            raise TransitionError("Approval score outside bounds")
    elif not isinstance(reason, str) or not reason.strip():
        raise TransitionError("Rejection reason is required")
