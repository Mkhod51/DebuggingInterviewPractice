"""Versioned record storage and atomic-state snapshot support."""
from copy import deepcopy
from dataclasses import dataclass
from .models import Entry, START


@dataclass
class Snapshot:
    entries: dict
    seen: set
    checkpoint: object

    def copy(self):
        return deepcopy(self)


class Store:
    def __init__(self):
        self._entries = {}
        self._seen = set()
        self.checkpoint = START

    def snapshot(self):
        return Snapshot(deepcopy(self._entries), set(self._seen), self.checkpoint)

    def restore(self, snapshot):
        snapshot = snapshot.copy()
        self._entries = snapshot.entries
        self._seen = snapshot.seen
        self.checkpoint = snapshot.checkpoint

    def entry(self, identifier):
        return deepcopy(self._entries.get(identifier))

    def records(self):
        return {id: deepcopy(entry.payload) for id, entry in sorted(self._entries.items()) if not entry.deleted}

    def seen(self, event_id):
        return event_id in self._seen

    def apply(self, event):
        if self.seen(event.id):
            return False
        current = self._entries.get(event.record_id)
        self._seen.add(event.id)
        if current is not None and event.revision >= current.revision:
            return False
        self._entries.pop(event.record_id, None) if event.kind == "delete" else self._entries.update({event.record_id: Entry(event.revision, deepcopy(event.payload))})
        return True

    def export(self):
        return dict(entries={id: entry.as_dict() for id, entry in sorted(self._entries.items())},
                    seen=sorted(self._seen), checkpoint=self.checkpoint.as_list())

    def counts(self):
        return dict(live=sum(not entry.deleted for entry in self._entries.values()),
                    deleted=sum(entry.deleted for entry in self._entries.values()),
                    seen=len(self._seen))
