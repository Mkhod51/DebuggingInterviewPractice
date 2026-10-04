"""Scripted local model transport."""
from copy import deepcopy
from .protocol import validate_call


class TransientError(RuntimeError):
    pass


class PermanentError(RuntimeError):
    pass


class FakeTransport:
    def __init__(self, scripts=None):
        self._scripts = deepcopy(scripts or {})
        self._calls = []

    def send(self, model, body):
        validate_call(body)
        self._calls.append(dict(model=model, body=deepcopy(body)))
        script = self._scripts.get(model, [])
        outcome = script.pop(0) if script else "success"
        if outcome == "transient":
            raise TransientError("Temporarily unavailable")
        if outcome == "permanent":
            raise PermanentError("Request refused")
        if isinstance(outcome, dict):
            return deepcopy(outcome)
        if outcome != "success":
            raise PermanentError("Invalid local outcome")
        return dict(request_id=body["request_id"], model=model, output=body["text"][::-1])

    @property
    def calls(self):
        return deepcopy(self._calls)

    def remaining(self, model):
        return deepcopy(self._scripts.get(model, []))

    def reset_calls(self):
        self._calls.clear()

    def summary(self):
        counts = {}
        for call in self._calls:
            counts[call["model"]] = counts.get(call["model"], 0) + 1
        return counts
