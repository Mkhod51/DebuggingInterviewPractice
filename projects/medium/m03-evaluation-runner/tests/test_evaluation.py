from pathlib import Path
import pytest
from practice_app.models import Case, Prediction
from practice_app.metrics import align, calculate, ProtocolError
from practice_app.model import FakeModel
from practice_app.service import EvaluationRunner, runner_from_file


def test_out_of_order_predictions_match_their_cases():
    cases = [Case("a", "one", "yes"), Case("b", "two", "no")]
    rows = align(cases, [Prediction("b", "no"), Prediction("a", "yes")])
    assert [row.actual for row in rows] == ["yes", "no"]
    assert all(row.correct for row in rows)


def test_accuracy_excludes_failed_predictions():
    cases = [Case("a", "one", "yes"), Case("b", "two", "no")]
    metrics = calculate(align(cases, [Prediction("a", "yes"), Prediction("b", error="offline")]))
    assert metrics.accuracy == 1.0
    assert metrics.coverage == 0.5 and metrics.failed == 1


def test_empty_and_all_error_runs_have_no_accuracy():
    assert EvaluationRunner(FakeModel([])).run([]).metrics.accuracy is None
    rows = align([Case("a", "one", "yes")], [])
    assert calculate(rows).accuracy is None


def test_duplicate_and_unknown_outputs_are_protocol_errors():
    case = Case("a", "one", "yes")
    for outputs in [[Prediction("a", "yes"), Prediction("a", "no")], [Prediction("b", "yes")]]:
        with pytest.raises(ProtocolError):
            align([case], outputs)


def test_batching_preserves_input_order_and_limits_calls():
    cases = [Case(str(i), str(i), "yes") for i in range(3)]
    model = FakeModel([Prediction(str(i), "yes") for i in range(3)])
    result = EvaluationRunner(model, 2).run(cases)
    assert [row.case_id for row in result.results] == ["0", "1", "2"]
    assert [len(call.case_ids) for call in model.calls] == [2, 1]


def test_duplicate_inputs_and_invalid_prediction_shape_are_errors():
    with pytest.raises(ValueError):
        EvaluationRunner(FakeModel([])).run([Case("x", "a", "b"), Case("x", "a", "b")])
    with pytest.raises(ValueError):
        Prediction("x", value="yes", error="bad")


def test_fixture_runner_end_to_end():
    runner, cases = runner_from_file(Path(__file__).resolve().parents[1] / "fixtures/evaluation.json", 3)
    result = runner.run(cases)
    assert [row.correct for row in result.results] == [True, True, None]
    assert result.metrics.accuracy == 1 and result.metrics.coverage == pytest.approx(2/3)
