"""Evaluation domain records and serialization."""
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class Case:
    id: str
    text: str
    expected: str

    def __post_init__(self):
        if not self.id:
            raise ValueError("Empty case ID")

    def as_dict(self):
        return dict(id=self.id, text=self.text, expected=self.expected)


@dataclass(frozen=True)
class Completion:
    case_id: str
    actual: str | None
    error: str | None

    def as_dict(self):
        return dict(case_id=self.case_id, actual=self.actual, error=self.error)


@dataclass(frozen=True)
class Result:
    case_id: str
    expected: str
    actual: str | None
    correct: bool | None
    error: str | None

    def as_dict(self):
        return dict(case_id=self.case_id, expected=self.expected, actual=self.actual,
                    correct=self.correct, error=self.error)


def validate_cases(cases):
    ids = [case.id for case in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate input ID")


def load_input(path):
    data = json.loads(Path(path).read_text())
    return [Case(**row) for row in data["cases"]], data["outcomes"], data["release_order"]
