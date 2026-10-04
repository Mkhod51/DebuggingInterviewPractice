"""Read-only operational views of synchronizer progress."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Progress:
    live_records: int
    tombstones: int
    distinct_events: int
    remaining_events: int
    checkpoint: tuple

    @property
    def caught_up(self):
        return self.remaining_events == 0

    def as_dict(self):
        return dict(live_records=self.live_records, tombstones=self.tombstones,
                    distinct_events=self.distinct_events, remaining_events=self.remaining_events,
                    checkpoint=list(self.checkpoint), caught_up=self.caught_up)


def progress(synchronizer):
    counts = synchronizer.store.counts()
    cursor = synchronizer.store.checkpoint
    return Progress(counts["live"], counts["deleted"], counts["seen"],
                    synchronizer.source.remaining(cursor), (cursor.timestamp, cursor.sequence))


def revisions(store):
    snapshot = store.snapshot()
    return {id: entry.revision for id, entry in sorted(snapshot.entries.items())}


def deleted_ids(store):
    return tuple(id for id, entry in sorted(store.snapshot().entries.items()) if entry.deleted)
