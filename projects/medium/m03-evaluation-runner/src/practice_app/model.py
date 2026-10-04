"""A scripted batch model with explicit output order."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Call:
    case_ids: tuple
    texts: tuple


class FakeModel:
    def __init__(self, predictions):
        self._predictions = tuple(predictions)
        self._calls = []

    def predict(self, cases):
        cases = list(cases)
        ids = {case.id for case in cases}
        self._calls.append(Call(tuple(case.id for case in cases), tuple(case.text for case in cases)))
        return [row for row in self._predictions if row.case_id in ids]

    @property
    def calls(self):
        return list(self._calls)

    def reset_calls(self):
        self._calls.clear()

    def configured_ids(self):
        return tuple(row.case_id for row in self._predictions)


class StaticModel:
    """Return one fixed response, useful for local protocol diagnostics."""
    def __init__(self, response):
        self.response = tuple(response)
        self.calls = 0

    def predict(self, cases):
        self.calls += 1
        return list(self.response)
