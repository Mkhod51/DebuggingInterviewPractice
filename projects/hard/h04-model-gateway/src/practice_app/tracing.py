"""Per-request trace ownership and operational views."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    request_id: str
    stage: str
    model: str | None
    attempt: int | None
    detail: str | None

    def as_dict(self):
        return dict(request_id=self.request_id, stage=self.stage, model=self.model,
                    attempt=self.attempt, detail=self.detail)


class Trace:
    def __init__(self, request_id):
        self.request_id = request_id
        self._events = []

    def record(self, stage, model=None, attempt=None, detail=None):
        self._events.append(Event(self.request_id, stage, model, attempt, detail))

    def events(self):
        return tuple(self._events)

    def attempts(self, model):
        return tuple(event for event in self._events if event.stage == "send" and event.model == model)

    def stages(self):
        return tuple(event.stage for event in self._events)

    def as_dict(self):
        return dict(request_id=self.request_id, events=[event.as_dict() for event in self._events])
