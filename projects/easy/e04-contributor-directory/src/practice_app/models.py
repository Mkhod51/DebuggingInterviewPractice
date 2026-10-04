"""Contributor directory records."""
from dataclasses import dataclass
import json
import math
from pathlib import Path


def normalize_email(email):
    return email.strip().casefold()


def validate_quality(value):
    if value is not None and (not math.isfinite(value) or not 0 <= value <= 1):
        raise ValueError("Quality outside bounds")


@dataclass(frozen=True)
class Contributor:
    id: str
    name: str
    email: str
    quality: float | None
    capacity: int = 0
    active: bool = True

    def __post_init__(self):
        if not self.id or not self.name or not normalize_email(self.email):
            raise ValueError("Missing profile identity")
        if self.capacity < 0:
            raise ValueError("Negative capacity")
        validate_quality(self.quality)

    def as_dict(self):
        return dict(id=self.id, name=self.name, email=self.email,
                    quality=self.quality, capacity=self.capacity, active=self.active)


def load_contributors(path):
    return [Contributor(**row) for row in json.loads(Path(path).read_text())]
