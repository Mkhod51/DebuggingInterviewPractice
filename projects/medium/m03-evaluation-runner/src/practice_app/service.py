"""Batch evaluation and JSON reporting."""
from dataclasses import dataclass
import json
from .metrics import align, calculate
from .model import FakeModel
from .models import load_input


@dataclass(frozen=True)
class Report:
    results: tuple
    metrics: object

    def as_dict(self):
        return dict(results=[row.as_dict() for row in self.results], metrics=self.metrics.as_dict())

    def to_json(self):
        return json.dumps(self.as_dict(), sort_keys=True)

    def failures(self):
        return tuple(row for row in self.results if row.error is not None)


class EvaluationRunner:
    def __init__(self, model, batch_size=2):
        if batch_size <= 0:
            raise ValueError("Batch size must be positive")
        self.model = model
        self.batch_size = batch_size

    def run(self, cases):
        cases = list(cases)
        ids = [case.id for case in cases]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate input ID")
        results = []
        for start in range(0, len(cases), self.batch_size):
            batch = cases[start:start+self.batch_size]
            predictions = self.model.predict(batch)
            results.extend(align(batch, predictions))
        return Report(tuple(results), calculate(results))


def runner_from_file(path, batch_size=2):
    cases, predictions = load_input(path)
    return EvaluationRunner(FakeModel(predictions), batch_size), cases
