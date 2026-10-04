"""Workflow entry points, fixture loading and event construction."""
import json
from pathlib import Path
from .models import WorkItem, Event, Clock
from . import transitions
from .store import Store
from .publisher import FakePublisher
from .audit import inspect


class Workflow:
    def __init__(self, store, publisher, clock):
        self.store = store
        self.publisher = publisher
        self.clock = clock

    def _transition(self, identifier, actor, expected_version, action, **kwargs):
        before = self.store.get(identifier)
        transform = getattr(transitions, action)
        after = transform(before, actor, expected_version, **kwargs)
        event = Event(identifier, after.version, action, actor, after.state, self.clock.now())
        return self.store.commit(before, after, event, self.publisher)

    def claim(self, identifier, actor, expected_version):
        return self._transition(identifier, actor, expected_version, "claim")

    def submit(self, identifier, actor, expected_version, data):
        return self._transition(identifier, actor, expected_version, "submit", data=data)

    def review(self, identifier, actor, expected_version, approved, score=None, reason=None):
        return self._transition(identifier, actor, expected_version, "review",
                                approved=approved, score=score, reason=reason)

    def requeue(self, identifier, actor, expected_version):
        return self._transition(identifier, actor, expected_version, "requeue")

    def execute(self, command):
        command = dict(command)
        action = command.pop("action")
        if action not in {"claim", "submit", "review", "requeue"}:
            raise ValueError("Unknown action")
        return getattr(self, action)(**command)

    def audit(self):
        return inspect(self.store)

    def available_actions(self, identifier):
        return transitions.available_actions(self.store.get(identifier))


def workflow_from_file(path):
    data = json.loads(Path(path).read_text())
    items = [WorkItem(**row) for row in data["items"]]
    engine = Workflow(Store(items), FakePublisher(), Clock(data.get("now", 0)))
    return engine, data["commands"]
