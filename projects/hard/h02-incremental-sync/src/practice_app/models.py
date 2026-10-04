"""Versioned stream records and sync result contracts."""
from copy import deepcopy
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True, order=True)
class Cursor:
    timestamp: int
    sequence: int

    def as_list(self):
        return [self.timestamp, self.sequence]


START = Cursor(-1, -1)


@dataclass(frozen=True)
class Event:
    id: str
    record_id: str
    revision: int
    timestamp: int
    sequence: int
    kind: str
    payload: dict | None = None

    def __post_init__(self):
        if not self.id or not self.record_id or self.revision < 0:
            raise ValueError("Invalid event identity")
        if self.timestamp < 0 or self.sequence < 0:
            raise ValueError("Invalid event cursor")
        if self.kind not in {"upsert", "delete"}:
            raise ValueError("Invalid event kind")
        if (self.kind == "upsert") != isinstance(self.payload, dict):
            raise ValueError("Payload must exist exactly for upserts")
        object.__setattr__(self, "payload", deepcopy(self.payload))

    @property
    def cursor(self):
        return Cursor(self.timestamp, self.sequence)

    def as_dict(self):
        return deepcopy(vars(self))


@dataclass(frozen=True)
class Entry:
    revision: int
    payload: dict | None

    @property
    def deleted(self):
        return self.payload is None

    def as_dict(self):
        return dict(revision=self.revision, payload=deepcopy(self.payload), deleted=self.deleted)


@dataclass(frozen=True)
class BatchResult:
    consumed: int
    applied: int
    checkpoint: Cursor

    def as_dict(self):
        return dict(consumed=self.consumed, applied=self.applied, checkpoint=self.checkpoint.as_list())


def load_events(path):
    return [Event(**row) for row in json.loads(Path(path).read_text())]
