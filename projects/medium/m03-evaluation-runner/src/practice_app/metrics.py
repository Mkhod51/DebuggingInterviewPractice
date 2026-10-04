"""Output association and aggregate metrics."""
from dataclasses import dataclass
from .models import Result


class ProtocolError(ValueError):
    pass


def align(cases, predictions):
    cases, predictions = list(cases), list(predictions)
    ids = {case.id for case in cases}
    output_ids = [row.case_id for row in predictions]
    if len(output_ids) != len(set(output_ids)):
        raise ProtocolError("Duplicate output ID")
    if set(output_ids) - ids:
        raise ProtocolError("Unknown output ID")
    by_id = dict(zip([case.id for case in cases], predictions))
    results = []
    for case in cases:
        output = by_id.get(case.id)
        if output is None:
            results.append(Result(case.id, case.expected, None, None, "missing prediction"))
        elif output.error is not None:
            results.append(Result(case.id, case.expected, None, None, output.error))
        else:
            results.append(Result(case.id, case.expected, output.value,
                                  output.value == case.expected, None))
    return results


@dataclass(frozen=True)
class Metrics:
    total: int
    scored: int
    failed: int
    correct: int
    accuracy: float | None
    coverage: float

    def as_dict(self):
        return dict(total=self.total, scored=self.scored, failed=self.failed,
                    correct=self.correct, accuracy=self.accuracy, coverage=self.coverage)


def calculate(results):
    results = list(results)
    scored = [row for row in results if row.error is None]
    correct = sum(row.correct for row in scored)
    accuracy = correct / len(results) if scored else None
    coverage = len(scored) / len(results) if results else 0.0
    return Metrics(len(results), len(scored), len(results)-len(scored), correct, accuracy, coverage)
