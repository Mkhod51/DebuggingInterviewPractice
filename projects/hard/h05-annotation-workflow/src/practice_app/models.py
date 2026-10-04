"""Persistent work items and versioned workflow events."""
from copy import deepcopy
from dataclasses import dataclass
import json

STATES = {"queued", "claimed", "submitted", "approved", "rejected"}


@dataclass(frozen=True)
class WorkItem:
    id: str
    state: str = "queued"
    version: int = 0
    owner: str | None = None
    submission: dict | None = None
    review: dict | None = None

    def __post_init__(self):
        if not self.id or self.state not in STATES or self.version < 0:
            raise ValueError("Invalid work item")
        if self.state == "queued" and any(value is not None for value in [self.owner, self.submission, self.review]):
            raise ValueError("Queued item retains work")
        if self.state != "queued" and not self.owner:
            raise ValueError("Owned state needs an owner")
        if self.state in {"submitted", "approved", "rejected"} and not self.submission:
            raise ValueError("Submitted state needs data")
        if self.state in {"approved", "rejected"} and self.review is None:
            raise ValueError("Reviewed state needs review")
        object.__setattr__(self, "submission", deepcopy(self.submission))
        object.__setattr__(self, "review", deepcopy(self.review))

    def as_dict(self):
        return deepcopy(vars(self))


@dataclass(frozen=True)
class Event:
    task_id: str
    version: int
    action: str
    actor: str
    state: str
    timestamp: int

    def as_dict(self):
        return dict(task_id=self.task_id, version=self.version, action=self.action,
                    actor=self.actor, state=self.state, timestamp=self.timestamp)


class Clock:
    def __init__(self, now=0):
        self._now = now

    def now(self):
        return self._now

    def advance(self, seconds):
        if seconds < 0:
            raise ValueError("Clock cannot move backwards")
        self._now += seconds


def validate_submission(data):
    if not isinstance(data, dict) or not data:
        raise ValueError("Submission must be a nonempty object")
    json.dumps(data, allow_nan=False)
