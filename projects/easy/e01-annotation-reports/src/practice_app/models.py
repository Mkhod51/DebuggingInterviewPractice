"""Validated annotation records and report windows."""
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class Annotation:
    id: str
    project: str
    status: str
    timestamp: int
    seconds: int

    def __post_init__(self):
        if not self.id or not self.project:
            raise ValueError("Identifiers cannot be empty")
        if self.status not in {"accepted", "pending", "rejected"}:
            raise ValueError("Unknown annotation status")
        if self.seconds < 0:
            raise ValueError("Negative annotation duration")

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def as_dict(self):
        return dict(id=self.id, project=self.project, status=self.status,
                    timestamp=self.timestamp, seconds=self.seconds)


@dataclass(frozen=True)
class Window:
    start: int
    end: int

    def __post_init__(self):
        if self.start >= self.end:
            raise ValueError("Window must have positive width")

    def contains(self, timestamp):
        return self.start < timestamp < self.end


def load_annotations(path):
    rows = json.loads(Path(path).read_text())
    records = [Annotation.from_dict(row) for row in rows]
    validate_unique(records)
    return records


def validate_unique(records):
    ids = [record.id for record in records]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate annotation ID")
