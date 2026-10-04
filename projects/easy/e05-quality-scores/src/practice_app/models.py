"""Validated quality reviews and summary values."""
from dataclasses import dataclass
import json
import math
from pathlib import Path


@dataclass(frozen=True)
class Review:
    id: str
    contributor: str
    score: float
    weight: float = 1.0

    def __post_init__(self):
        if not self.id or not self.contributor:
            raise ValueError("Missing identifier")
        if not math.isfinite(self.score) or not 0 <= self.score <= 1:
            raise ValueError("Invalid score")
        if not math.isfinite(self.weight) or self.weight <= 0:
            raise ValueError("Invalid weight")

    def as_dict(self):
        return dict(id=self.id, contributor=self.contributor, score=self.score, weight=self.weight)


@dataclass(frozen=True)
class Summary:
    count: int
    total_weight: float
    mean: float | None

    def as_dict(self):
        return dict(count=self.count, total_weight=self.total_weight,
                    mean=None if self.mean is None else round(self.mean, 4))


def load_reviews(path):
    return [Review(**row) for row in json.loads(Path(path).read_text())]
