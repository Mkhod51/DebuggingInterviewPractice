"""Job state and retry policy."""
from dataclasses import dataclass
from copy import deepcopy


@dataclass
class Job:
    id: str
    payload: dict
    due_at: int = 0
    status: str = "queued"
    attempts: int = 0
    result: dict | None = None
    error: str | None = None

    def __post_init__(self):
        if not self.id or self.status not in {"queued", "running", "retry_wait", "succeeded", "failed"}:
            raise ValueError("Invalid job")
        if self.attempts < 0:
            raise ValueError("Negative attempt count")

    def copy(self):
        return deepcopy(self)

    def as_dict(self):
        return deepcopy(vars(self))

    @property
    def terminal(self):
        return self.status in {"succeeded", "failed"}


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3
    base_delay: int = 2

    def __post_init__(self):
        if self.max_attempts <= 0 or self.base_delay <= 0:
            raise ValueError("Retry policy must be positive")

    def can_retry(self, attempts):
        return attempts <= self.max_attempts

    def due(self, now, attempts):
        return self.base_delay * 2 ** (attempts - 1)


class Clock:
    def __init__(self, now=0):
        self._now = now

    def now(self):
        return self._now

    def advance(self, seconds):
        if seconds < 0:
            raise ValueError("Clock cannot move backwards")
        self._now += seconds
