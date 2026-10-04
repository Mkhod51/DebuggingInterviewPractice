"""Task state and local event ledger committed together."""
from copy import deepcopy
from .policy import VersionConflict


class Store:
    def __init__(self, items):
        items = list(items)
        self._items = {item.id: deepcopy(item) for item in items}
        if len(self._items) != len(items):
            raise ValueError("Duplicate task ID")
        self._events = []

    def get(self, identifier):
        return deepcopy(self._items[identifier])

    def all(self):
        return [deepcopy(item) for id, item in sorted(self._items.items())]

    def events(self, identifier=None):
        return [deepcopy(event) for event in self._events
                if identifier is None or event.task_id == identifier]

    def commit(self, before, after, event, publisher):
        current = self._items[before.id]
        if current.version != before.version:
            raise VersionConflict("Task changed before commit")
        if after.id != before.id or after.version != before.version+1:
            raise ValueError("Invalid state version")
        if event.task_id != after.id or event.version != after.version or event.state != after.state:
            raise ValueError("Event differs from task state")
        before_events = self._events
        try:
            self._items[before.id] = deepcopy(after)
            self._events.append(deepcopy(event))
            publisher.publish(event)
        except Exception:
            self._items[before.id] = deepcopy(before)
            self._events = before_events
            raise
        return self.get(after.id)

    def export(self):
        return dict(items=[item.as_dict() for item in self.all()],
                    events=[event.as_dict() for event in self.events()])

    def versions(self):
        return {item.id: item.version for item in self.all()}
