"""Evaluation inputs, outputs and result records."""
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


@dataclass(frozen=True)
class Prediction:
    case_id: str
    value: str | None = None
    error: str | None = None

    def __post_init__(self):
        if not self.case_id or (self.value is None) == (self.error is None):
            raise ValueError("Prediction needs exactly one value or error")

    def as_dict(self):
        return dict(case_id=self.case_id, value=self.value, error=self.error)


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


def load_input(path):
    data = json.loads(Path(path).read_text())
    return ([Case(**row) for row in data["cases"]],
            [Prediction(**row) for row in data["predictions"]])
