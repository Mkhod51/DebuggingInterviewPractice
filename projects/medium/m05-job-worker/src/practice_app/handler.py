"""A deterministic handler consuming per-job outcome scripts."""
from copy import deepcopy


class RetryableError(RuntimeError):
    pass


class PermanentError(RuntimeError):
    pass


class FakeHandler:
    def __init__(self, scripts):
        self._scripts = deepcopy(scripts)
        self._calls = []

    def execute(self, job):
        self._calls.append(job.id)
        outcomes = self._scripts.get(job.id, [])
        if not outcomes:
            raise PermanentError("No configured outcome")
        outcome = outcomes.pop(0)
        if outcome == "temporary":
            raise RetryableError("Temporary processing failure")
        if outcome == "permanent":
            raise PermanentError("Invalid payload")
        if not isinstance(outcome, dict):
            raise ValueError("Unexpected handler outcome")
        return deepcopy(outcome)

    @property
    def calls(self):
        return list(self._calls)

    def remaining(self, identifier):
        return deepcopy(self._scripts.get(identifier, []))
