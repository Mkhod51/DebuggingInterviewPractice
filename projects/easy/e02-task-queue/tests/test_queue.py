from pathlib import Path
import pytest
from practice_app.models import Task
from practice_app.queue import Queue
from practice_app.service import QueueService, service_from_file


def task(id, priority=1, available=0, enabled=True):
    return Task(id, priority, 0, available, enabled)


def test_urgent_jobs_are_selected_first():
    queue = Queue([task("low", 1), task("high", 9)])
    assert [row.id for row in queue.ordered()] == ["high", "low"]


def test_unready_jobs_do_not_consume_dispatch_slots():
    service = QueueService(Queue([task("a", available=20), task("b"), task("c")]))
    assert [row.id for row in service.dispatch(10, 2).tasks] == ["b", "c"]
    assert service.queue.get("a") is not None


def test_ties_are_stable_by_creation_and_id():
    rows = [Task("z", 2, 1, 1), Task("b", 2, 0, 0), Task("a", 2, 0, 0)]
    assert [row.id for row in Queue(rows).ordered()] == ["a", "b", "z"]


def test_zero_slots_and_peek_preserve_queue():
    service = QueueService(Queue([task("a")]))
    assert service.dispatch(0, 0).tasks == ()
    assert len(service.peek(0, 1)) == len(service.queue) == 1


def test_negative_limit_and_duplicates_are_rejected():
    service = QueueService(Queue([task("a")]))
    with pytest.raises(ValueError):
        service.dispatch(0, -1)
    with pytest.raises(ValueError):
        service.enqueue(task("a"))


def test_summary_and_cancellation():
    service = QueueService(Queue([task("a"), task("b", enabled=False), task("c", available=20)]))
    assert service.summary(10) == {"total": 3, "ready": 1, "disabled": 1, "waiting": 1}
    assert not service.cancel("unknown")
    assert service.cancel("b")


def test_fixture_dispatch_end_to_end():
    service = service_from_file(Path(__file__).resolve().parents[1] / "fixtures/queue.json")
    assert [row.id for row in service.dispatch(10, 2).tasks] == ["urgent", "ordinary"]
    assert service.summary(10)["total"] == 1
