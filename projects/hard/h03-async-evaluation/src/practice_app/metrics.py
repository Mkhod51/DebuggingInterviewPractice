"""Quality and operational reporting."""
from dataclasses import dataclass
import json


@dataclass(frozen=True)
class Metrics:
    total: int
    successful: int
    failed: int
    correct: int
    accuracy: float | None
    coverage: float

    def as_dict(self):
        return dict(total=self.total, successful=self.successful, failed=self.failed,
                    correct=self.correct, accuracy=self.accuracy, coverage=self.coverage)


def calculate(results):
    results = list(results)
    successful = [row for row in results if row.error is None]
    correct = sum(row.correct for row in successful)
    return Metrics(len(results), len(successful), len(results)-len(successful), correct,
                   correct/len(successful) if successful else None,
                   len(successful)/len(results) if results else 0.0)


@dataclass(frozen=True)
class Report:
    results: tuple
    metrics: Metrics

    def as_dict(self):
        return dict(results=[row.as_dict() for row in self.results], metrics=self.metrics.as_dict())

    def to_json(self):
        return json.dumps(self.as_dict(), sort_keys=True)

    def result(self, identifier):
        return next((row for row in self.results if row.case_id == identifier), None)
