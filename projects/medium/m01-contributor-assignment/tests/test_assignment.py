from pathlib import Path
import pytest
from practice_app.models import Contributor, Task
from practice_app.repository import Repository
from practice_app.rules import assess
from practice_app.service import AssignmentService, service_from_file


def worker(id="a", capacity=10, skills=("text", "audit")):
    return Contributor(id, frozenset(skills), frozenset({"en"}), capacity)


def task(id="t", units=1, skills=("text",)):
    return Task(id, frozenset(skills), "en", units)


def test_all_required_skills_are_necessary():
    assert not assess(worker(skills=("text",)), task(skills=("text", "audit")), 0).eligible


def test_exact_capacity_is_available():
    result = AssignmentService(Repository([worker(capacity=2)])).assign([task(units=2)])
    assert result.unassigned == ()
    assert len(result.assignments) == 1


def test_weighted_assignments_consume_their_units():
    repository = Repository([worker()])
    repository.record(task(units=3), worker())
    assert repository.load("a") == 3
    assert repository.remaining("a") == 7


def test_inactive_or_wrong_language_is_rejected():
    contributor = Contributor("x", frozenset({"text"}), frozenset({"fr"}), 10, False)
    assert set(assess(contributor, task(), 0).reasons) == {"inactive", "language"}


def test_duplicate_batch_ids_are_errors():
    service = AssignmentService(Repository([worker()]))
    with pytest.raises(ValueError):
        service.assign([task(), task()])


def test_assignment_is_idempotent_and_release_frees_units():
    repository = Repository([worker()])
    service = AssignmentService(repository)
    first = service.assign([task(units=3)])
    assert service.assign([task(units=3)]) == first
    assert service.release("t")
    assert repository.load("a") == 0
    assert not service.release("t")


def test_ties_use_identifier_and_returned_lists_are_independent():
    repository = Repository([worker("b"), worker("a")])
    result = AssignmentService(repository).assign([task()])
    assert result.assignments[0].contributor_id == "a"
    repository.assignments().clear()
    assert len(repository.assignments()) == 1


def test_fixture_assignment_end_to_end():
    path = Path(__file__).resolve().parents[1] / "fixtures/batch.json"
    service, tasks = service_from_file(path)
    result = service.assign(tasks)
    assert [row.contributor_id for row in result.assignments] == ["qualified"]
    assert result.unassigned == ("large",)
    assert service.repository.load("qualified") == 3
