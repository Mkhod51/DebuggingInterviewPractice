"""Deterministic local API with recorded calls and scripted failures."""
from copy import deepcopy
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class Request:
    dataset: str
    cursor: str | None
    page_size: int

    def as_dict(self):
        return dict(dataset=self.dataset, cursor=self.cursor, page_size=self.page_size)


class FakeAPI:
    def __init__(self, datasets, failures=None):
        self._datasets = deepcopy(datasets)
        self._failures = dict(failures or {})
        self._calls = []

    def fetch_page(self, dataset, cursor, page_size):
        if page_size <= 0:
            raise ValueError("Page size must be positive")
        self._calls.append(Request(dataset, cursor, page_size))
        failure = self._failures.pop((dataset, cursor), None)
        if failure is not None:
            raise failure
        if dataset not in self._datasets:
            raise KeyError("Unknown dataset")
        key = "__first__" if cursor is None else cursor
        pages = self._datasets[dataset]
        if key not in pages:
            raise KeyError("Unknown cursor")
        return deepcopy(pages[key])

    @property
    def calls(self):
        return list(self._calls)

    def call_summary(self):
        result = {}
        for call in self._calls:
            result[call.dataset] = result.get(call.dataset, 0) + 1
        return result

    def reset_calls(self):
        self._calls.clear()

    @classmethod
    def from_file(cls, path):
        return cls(json.loads(Path(path).read_text()))
