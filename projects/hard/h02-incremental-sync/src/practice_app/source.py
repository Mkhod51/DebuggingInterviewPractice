"""A local ordered stream with independent pages."""
from copy import deepcopy


class FetchFailure(RuntimeError):
    pass


class EventSource:
    def __init__(self, events):
        events = list(events)
        cursors = [event.cursor for event in events]
        if len(cursors) != len(set(cursors)):
            raise ValueError("Duplicate stream cursor")
        self._events = tuple(sorted(deepcopy(events), key=lambda event: event.cursor))
        self._calls = []
        self._fail_next = False

    def fetch(self, cursor, limit):
        if limit <= 0:
            raise ValueError("Batch size must be positive")
        self._calls.append((cursor, limit))
        if self._fail_next:
            self._fail_next = False
            raise FetchFailure("Local stream unavailable")
        eligible = [event for event in self._events if event.cursor.timestamp > cursor.timestamp]
        return deepcopy(eligible[:limit])

    def fail_next(self):
        self._fail_next = True

    @property
    def calls(self):
        return list(self._calls)

    def remaining(self, cursor):
        return sum(event.cursor > cursor for event in self._events)

    def export(self):
        return [event.as_dict() for event in self._events]
