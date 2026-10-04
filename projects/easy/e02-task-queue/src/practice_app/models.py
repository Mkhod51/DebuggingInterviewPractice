"""Queue data and fixture loading."""
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class Task:
    id: str
    priority: int
    created_at: int
    available_at: int
    enabled: bool = True
    payload: str = ""

    def __post_init__(self):
        if not self.id:
            raise ValueError("Empty task ID")
        if self.available_at < self.created_at:
            raise ValueError("Availability predates creation")

    def as_dict(self):
        return dict(id=self.id, priority=self.priority, created_at=self.created_at,
                    available_at=self.available_at, enabled=self.enabled, payload=self.payload)

    def ready(self, now):
        return self.enabled and self.available_at <= now


def load_tasks(path):
    rows = json.loads(Path(path).read_text())
    return [Task(**row) for row in rows]


def validate_limit(limit):
    if limit < 0:
        raise ValueError("Negative slot limit")
