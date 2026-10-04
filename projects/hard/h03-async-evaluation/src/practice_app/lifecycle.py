"""Per-run lifecycle observation for local cancellation diagnostics."""
import asyncio
from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    stage: str
    case_id: str | None = None

    def as_dict(self):
        return dict(stage=self.stage, case_id=self.case_id)


class Lifecycle:
    def __init__(self):
        self.cleanup_started = asyncio.Event()
        self.finished = asyncio.Event()
        self._events = []

    def record(self, stage, case_id=None):
        self._events.append(Event(stage, case_id))
        if stage == "cleanup":
            self.cleanup_started.set()
        elif stage == "finished":
            self.finished.set()

    def events(self):
        return tuple(self._events)

    def as_dict(self):
        return dict(events=[event.as_dict() for event in self._events],
                    finished=self.finished.is_set())
