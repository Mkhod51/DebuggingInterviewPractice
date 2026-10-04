from pathlib import Path
import pytest
from practice_app.models import WorkItem, Clock
from practice_app.policy import TransitionError, VersionConflict
from practice_app.transitions import review, requeue
from practice_app.store import Store
from practice_app.publisher import FakePublisher, PublishFailure
from practice_app.engine import Workflow, workflow_from_file


def engine():
    return Workflow(Store([WorkItem("task")]), FakePublisher(), Clock(10))


def submitted():
    return WorkItem("task", "submitted", 2, "owner", {"label": "yes"})


def test_owner_can_submit_claimed_work():
    app = engine()
    app.claim("task", "owner", 0)
    item = app.submit("task", "owner", 1, {"label": "yes"})
    assert item.state == "submitted" and item.version == 2


def test_rejection_records_rejected_state():
    item = review(submitted(), "reviewer", 2, False, reason="needs another pass")
    assert item.state == "rejected"
    assert item.review["score"] is None


def test_requeue_clears_previous_work():
    item = WorkItem("task", "rejected", 3, "owner", {"label": "yes"}, {"reason": "wrong"})
    queued = requeue(item, "operator", 3)
    assert queued.state == "queued"
    assert (queued.owner, queued.submission, queued.review) == (None, None, None)


def test_failed_publication_restores_task_and_event_ledger():
    app = engine()
    before = app.store.export()
    app.publisher.fail_next()
    with pytest.raises(PublishFailure):
        app.claim("task", "owner", 0)
    assert app.store.export() == before
    assert app.publisher.events() == []
    assert app.claim("task", "owner", 0).version == 1
    assert app.audit().consistent


def test_stale_versions_and_double_claim_leave_state_unchanged():
    app = engine()
    app.claim("task", "owner", 0)
    before = app.store.export()
    with pytest.raises(VersionConflict):
        app.claim("task", "other", 0)
    with pytest.raises(TransitionError):
        app.claim("task", "other", 1)
    assert app.store.export() == before


def test_approval_zero_and_self_review_rules():
    assert review(submitted(), "reviewer", 2, True, score=0).review["score"] == 0
    with pytest.raises(TransitionError):
        review(submitted(), "owner", 2, True, score=1)
    with pytest.raises(TransitionError):
        review(submitted(), "reviewer", 2, False, reason="")


def test_snapshots_and_submission_data_are_independent():
    item = submitted()
    store = Store([item])
    snapshot = store.get("task")
    snapshot.submission["label"] = "edited"
    assert store.get("task").submission == {"label": "yes"}


def test_fixture_workflow_end_to_end():
    app, commands = workflow_from_file(Path(__file__).resolve().parents[1] / "fixtures/workflow.json")
    for command in commands:
        app.execute(command)
    item = app.store.get("task")
    assert item.state == "approved" and item.version == 7
    assert item.owner == "second" and item.submission == {"label": "no"}
    assert app.audit().consistent and app.audit().events == 7
