"""Local event publication with a controlled pre-publication failure."""
from copy import deepcopy


class PublishFailure(RuntimeError):
    pass


class FakePublisher:
    def __init__(self):
        self._events = []
        self._fail_next = False

    def fail_next(self):
        self._fail_next = True

    def publish(self, event):
        if self._fail_next:
            self._fail_next = False
            raise PublishFailure("Publication unavailable")
        self._events.append(deepcopy(event))

    def events(self):
        return deepcopy(self._events)

    def count(self, identifier=None):
        return sum(identifier is None or event.task_id == identifier for event in self._events)
