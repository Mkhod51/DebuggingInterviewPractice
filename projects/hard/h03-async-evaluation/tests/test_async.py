import asyncio
from pathlib import Path
import pytest
from practice_app.models import Case, Completion
from practice_app.association import associate, AssociationError
from practice_app.controlled_model import ControlledModel
from practice_app.runner import AsyncRunner
from practice_app.service import run_controlled, evaluate_file


def cases():
    return [Case("a", "one", "yes"), Case("b", "two", "no")]


def test_completion_order_does_not_change_result_identity():
    report = asyncio.run(run_controlled(cases(), {"a": {"value": "yes"}, "b": {"value": "no"}}, ["b", "a"]))
    assert [row.actual for row in report.results] == ["yes", "no"]
    assert report.metrics.accuracy == 1


def test_model_failure_is_a_case_error_not_a_scored_prediction():
    model = ControlledModel({"a": {"error": "offline"}}, automatic=True)
    report = asyncio.run(AsyncRunner(model).run([Case("a", "one", "yes")]))
    assert report.results[0].correct is None
    assert report.results[0].error == "offline"
    assert report.metrics.accuracy is None


def test_configured_concurrency_is_respected():
    async def scenario():
        model = ControlledModel({"a": {"value": "yes"}, "b": {"value": "no"}})
        runner = AsyncRunner(model, 1)
        run = asyncio.create_task(runner.run(cases()))
        first = await model.next_started()
        model.release(first)
        await model.next_finished()
        second = await model.next_started()
        model.release(second)
        await model.next_finished()
        await run
        assert model.peak == 1 and model.active == 0
    asyncio.run(scenario())


def test_cancelled_run_cancels_and_awaits_children():
    async def scenario():
        model = ControlledModel({"a": {"value": "yes"}, "b": {"value": "no"}})
        runner = AsyncRunner(model, 2)
        run = asyncio.create_task(runner.run(cases()))
        await model.next_started()
        await model.next_started()
        run.cancel()
        await runner.lifecycle.cleanup_started.wait()
        model.release_all()
        with pytest.raises(asyncio.CancelledError):
            await run
        assert set(model.cancelled) == {"a", "b"}
        assert model.active == 0 and not runner.running
        assert runner.lifecycle.finished.is_set()
    asyncio.run(scenario())


def test_empty_run_and_invalid_inputs():
    runner = AsyncRunner(ControlledModel({}))
    report = asyncio.run(runner.run([]))
    assert report.results == () and report.metrics.coverage == 0
    with pytest.raises(ValueError):
        AsyncRunner(ControlledModel({}), 0)
    with pytest.raises(ValueError):
        asyncio.run(runner.run([Case("a", "x", "x"), Case("a", "x", "x")]))


def test_association_rejects_missing_or_duplicate_completion_ids():
    with pytest.raises(AssociationError):
        associate(cases(), [Completion("a", "yes", None)])
    with pytest.raises(AssociationError):
        associate(cases(), [Completion("a", "yes", None), Completion("a", "yes", None)])


def test_runner_reusable_after_success():
    runner = AsyncRunner(ControlledModel({"a": {"value": "yes"}}, automatic=True))
    assert asyncio.run(runner.run([cases()[0]])).metrics.accuracy == 1
    assert asyncio.run(runner.run([cases()[0]])).metrics.accuracy == 1


def test_fixture_async_evaluation_end_to_end():
    report = evaluate_file(Path(__file__).resolve().parents[1] / "fixtures/evaluation.json")
    assert [row.case_id for row in report.results] == ["a", "b", "c"]
    assert [row.correct for row in report.results] == [True, True, None]
    assert report.metrics.failed == 1 and report.metrics.accuracy == 1
