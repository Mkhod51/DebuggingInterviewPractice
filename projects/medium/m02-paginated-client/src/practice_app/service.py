"""Dataset export entry point."""
from dataclasses import dataclass
import json
from .api import FakeAPI
from .pagination import traverse, collect


@dataclass(frozen=True)
class DatasetResult:
    dataset: str
    records: tuple
    page_count: int
    cursors: tuple

    def as_dict(self):
        return dict(dataset=self.dataset, records=[row.as_dict() for row in self.records],
                    page_count=self.page_count, cursors=list(self.cursors))

    def to_json(self):
        return json.dumps(self.as_dict(), sort_keys=True)

    def find(self, identifier):
        return next((row.as_dict() for row in self.records if row.id == identifier), None)


class DatasetClient:
    def __init__(self, api, max_pages=100):
        if max_pages <= 0:
            raise ValueError("Page limit must be positive")
        self.api = api
        self.max_pages = max_pages

    def fetch(self, dataset, page_size=20):
        traversal = traverse(self.api, dataset, page_size, self.max_pages)
        return DatasetResult(dataset, collect(traversal), traversal.page_count, traversal.cursors)

    def export(self, dataset, page_size=20):
        return self.fetch(dataset, page_size).to_json()


def client_from_file(path, max_pages=100):
    return DatasetClient(FakeAPI.from_file(path), max_pages)
