"""Domain records for the contributor assignment service."""
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class Contributor:
    id: str
    skills: frozenset
    languages: frozenset
    capacity: int
    active: bool = True

    def __post_init__(self):
        if not self.id or self.capacity < 0:
            raise ValueError("Invalid contributor")

    @classmethod
    def from_dict(cls, row):
        return cls(row["id"], frozenset(row["skills"]),
                   frozenset(row["languages"]), row["capacity"], row.get("active", True))

    def as_dict(self):
        return dict(id=self.id, skills=sorted(self.skills), languages=sorted(self.languages),
                    capacity=self.capacity, active=self.active)


@dataclass(frozen=True)
class Task:
    id: str
    skills: frozenset
    language: str
    units: int = 1

    def __post_init__(self):
        if not self.id or not self.language or self.units <= 0:
            raise ValueError("Invalid task")

    @classmethod
    def from_dict(cls, row):
        return cls(row["id"], frozenset(row["skills"]), row["language"], row.get("units", 1))

    def as_dict(self):
        return dict(id=self.id, skills=sorted(self.skills), language=self.language, units=self.units)


@dataclass(frozen=True)
class Assignment:
    task_id: str
    contributor_id: str
    units: int

    def as_dict(self):
        return dict(task_id=self.task_id, contributor_id=self.contributor_id, units=self.units)


def load_input(path):
    data = json.loads(Path(path).read_text())
    contributors = [Contributor.from_dict(row) for row in data["contributors"]]
    tasks = [Task.from_dict(row) for row in data["tasks"]]
    return contributors, tasks
