from pathlib import Path
import pytest
from practice_app.models import Contributor, Project, Task, Allocation
from practice_app.eligibility import assess
from practice_app.planner import Plan, build_plan
from practice_app.repository import Repository, CommitFailure
from practice_app.service import AllocationService, service_from_file


def worker(capacity=10):
    return Contributor("w", frozenset({"p"}), frozenset({"text"}), frozenset({"en"}), capacity)


def task(id, units=1, priority=0):
    return Task(id, "p", frozenset({"text"}), "en", units, priority)


def repo(capacity=10, quota=10):
    return Repository([worker(capacity)], [Project("p", quota)])


def test_project_authorization_uses_project_membership():
    repository = repo()
    assert assess(worker(), task("t"), Project("p", 10), repository.snapshot()).allowed


def test_plans_reserve_all_prior_tasks():
    repository = repo(capacity=2)
    plan = build_plan([worker(2)], repository.projects,
                      [task("a"), task("b"), task("c")], repository.snapshot())
    assert [row.task_id for row in plan.allocations] == ["a", "b"]
    assert plan.unallocated == ("c",)


def test_failed_publication_restores_every_state_component():
    repository = repo()
    plan = Plan((Allocation("a", "p", "w", 2), Allocation("b", "p", "w", 2)), ())
    before = repository.snapshot()
    with pytest.raises(CommitFailure):
        repository.commit(plan, fail_task="b")
    assert repository.snapshot() == before


def test_repeated_runs_ignore_already_assigned_tasks():
    service = AllocationService(repo())
    service.run([task("a")])
    before = service.repository.snapshot()
    assert service.run([task("a")]).plan.allocations == ()
    assert service.repository.snapshot() == before


def test_priority_and_quota_control_selection():
    service = AllocationService(repo(quota=1))
    result = service.run([task("low", priority=1), task("high", priority=9)])
    assert [row.task_id for row in result.plan.allocations] == ["high"]
    assert result.plan.unallocated == ("low",)


def test_preview_does_not_change_repository():
    service = AllocationService(repo())
    before = service.repository.snapshot()
    service.preview([task("a")])
    assert service.repository.snapshot() == before


def test_snapshot_is_independent():
    repository = repo()
    repository.snapshot().loads["w"] = 100
    assert repository.snapshot().loads["w"] == 0


def test_invalid_batches_are_rejected():
    service = AllocationService(repo())
    with pytest.raises(ValueError):
        service.run([task("a"), task("a")])
    with pytest.raises(ValueError):
        service.run([Task("a", "unknown", frozenset(), "en", 1)])


def test_zero_quota_and_inactive_contributors_are_ineligible():
    repository = repo(quota=0)
    assert not assess(worker(), task("a"), Project("p", 0), repository.snapshot()).allowed
    inactive = Contributor("w", frozenset({"p"}), frozenset({"text"}), frozenset({"en"}), 10, False)
    assert not assess(inactive, task("a"), Project("p", 10), repository.snapshot()).allowed


def test_fixture_pipeline_end_to_end():
    service, tasks = service_from_file(Path(__file__).resolve().parents[1] / "fixtures/batch.json")
    result = service.run(tasks)
    assert [row.task_id for row in result.plan.allocations] == ["a", "b"]
    assert result.plan.unallocated == ("c",)
    assert result.audit.consistent
    assert result.audit.assigned_units == 2
    assert service.release("a")
    assert service.audit().assigned_units == 1
