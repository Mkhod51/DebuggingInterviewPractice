from pathlib import Path
import pytest
from practice_app.models import Job, Clock, RetryPolicy
from practice_app.repository import Repository
from practice_app.handler import FakeHandler
from practice_app.worker import Worker
from practice_app.service import worker_from_file


def worker(outcomes, now=0, max_attempts=3):
    return Worker(Repository([Job("a", {})]), FakeHandler({"a": outcomes}), Clock(now), RetryPolicy(max_attempts, 2))


def test_retry_budget_includes_first_attempt():
    app = worker(["temporary"] * 4, max_attempts=2)
    app.tick()
    app.clock.advance(2)
    app.tick()
    assert app.repository.get("a").status == "failed"
    app.clock.advance(100)
    app.tick()
    assert app.handler.calls == ["a", "a"]


def test_permanent_errors_are_terminal():
    app = worker(["permanent", {"ok": True}])
    app.tick()
    assert app.repository.get("a").status == "failed"
    app.clock.advance(10)
    app.tick()
    assert app.handler.calls == ["a"]


def test_retry_deadline_is_relative_to_failure_time():
    app = worker(["temporary", {"ok": True}], now=100)
    app.tick()
    assert app.repository.get("a").due_at == 102
    assert app.tick().processed == ()
    app.clock.advance(2)
    assert app.tick().processed == ("a",)


def test_success_is_terminal_and_result_is_independent():
    app = worker([{"items": [1]}])
    app.tick()
    snapshot = app.repository.get("a")
    snapshot.result["items"].clear()
    assert app.repository.get("a").result == {"items": [1]}
    assert app.tick().processed == ()


def test_duplicate_jobs_and_invalid_policy_are_errors():
    with pytest.raises(ValueError):
        Repository([Job("a", {}), Job("a", {})])
    with pytest.raises(ValueError):
        RetryPolicy(0, 1)


def test_ready_ids_respect_time_and_identifier():
    repository = Repository([Job("b", {}, 5), Job("a", {}, 5), Job("c", {}, 6)])
    assert repository.ready_ids(5) == ["a", "b"]


def test_unexpected_errors_are_terminal():
    app = worker(["invalid"])
    app.tick()
    assert app.repository.get("a").status == "failed"


def test_fixture_worker_end_to_end():
    app = worker_from_file(Path(__file__).resolve().parents[1] / "fixtures/jobs.json")
    app.tick()
    assert app.repository.get("retry").due_at == 52
    assert app.repository.get("bad").status == "failed"
    app.clock.advance(2)
    app.tick()
    assert app.repository.get("retry").status == "succeeded"
    assert app.repository.get("retry").attempts == 2
