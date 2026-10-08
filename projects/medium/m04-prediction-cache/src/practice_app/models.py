"""Prediction identity and controlled time."""
from dataclasses import dataclass
from copy import deepcopy
import json


@dataclass(frozen=True)
class Request:
    model: str
    version: str
    text: str
    options: dict

    def __post_init__(self):
        if not self.model or not self.version:
            raise ValueError("Model and version are required")
        json.dumps(self.options, allow_nan=False)
        object.__setattr__(self, "options", deepcopy(self.options))

    def key(self):
        options = json.dumps(self.options, sort_keys=True, separators=(",", ":"), allow_nan=False)
        return (self.model, self.version, self.text, options)

    def as_dict(self):
        return dict(model=self.model, version=self.version, text=self.text, options=deepcopy(self.options))


class Clock:
    def __init__(self, now=0):
        self._now = now

    def now(self):
        return self._now

    def advance(self, seconds):
        if seconds < 0:
            raise ValueError("Clock cannot move backwards")
        self._now += seconds
        return self._now


@dataclass(frozen=True)
class Stats:
    hits: int
    misses: int
    backend_calls: int

    def as_dict(self):
        return dict(hits=self.hits, misses=self.misses, backend_calls=self.backend_calls)
