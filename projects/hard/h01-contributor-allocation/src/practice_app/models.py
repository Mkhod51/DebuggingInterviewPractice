"""Validated records at the allocation boundary."""
from dataclasses import dataclass, field
import json
from pathlib import Path


@dataclass(frozen=True)
class Contributor:
    id: str
    projects: frozenset
    certifications: frozenset
    languages: frozenset
    capacity: int
    active: bool = True

    def __post_init__(self):
        if not self.id or self.capacity < 0:
            raise ValueError("Invalid contributor")

    @classmethod
    def from_dict(cls, row):
        return cls(row["id"], frozenset(row["projects"]), frozenset(row["certifications"]),
                   frozenset(row["languages"]), row["capacity"], row.get("active", True))


@dataclass(frozen=True)
class Project:
    id: str
    quota: int

    def __post_init__(self):
        if not self.id or self.quota < 0:
            raise ValueError("Invalid project")


@dataclass(frozen=True)
class Task:
    id: str
    project: str
    certifications: frozenset
    language: str
    units: int
    priority: int = 0

    def __post_init__(self):
        if not self.id or not self.project or self.units <= 0:
            raise ValueError("Invalid task")

    @classmethod
    def from_dict(cls, row):
        return cls(row["id"], row["project"], frozenset(row["certifications"]),
                   row["language"], row["units"], row.get("priority", 0))


@dataclass(frozen=True)
class Allocation:
    task_id: str
    project_id: str
    contributor_id: str
    units: int

    def as_dict(self):
        return dict(task_id=self.task_id, project_id=self.project_id,
                    contributor_id=self.contributor_id, units=self.units)


@dataclass
class State:
    assignments: dict = field(default_factory=dict)
    loads: dict = field(default_factory=dict)
    usage: dict = field(default_factory=dict)

    def copy(self):
        return State(dict(self.assignments), dict(self.loads), dict(self.usage))


def load_input(path):
    data = json.loads(Path(path).read_text())
    return ([Contributor.from_dict(row) for row in data["contributors"]],
            [Project(**row) for row in data["projects"]],
            [Task.from_dict(row) for row in data["tasks"]])
