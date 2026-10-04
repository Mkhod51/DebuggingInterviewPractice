from pathlib import Path
import pytest
from practice_app.models import Event, Cursor
from practice_app.source import EventSource, FetchFailure
from practice_app.store import Store
from practice_app.synchronizer import Synchronizer, ApplyFailure
from practice_app.service import synchronizer_from_file, report


def event(id, revision=1, timestamp=10, sequence=1, kind="upsert", record="r"):
    return Event(id, record, revision, timestamp, sequence, kind, None if kind == "delete" else {"v": revision})


def test_same_timestamp_events_remain_after_checkpoint():
    source = EventSource([event("a", sequence=1), event("b", sequence=2)])
    assert [row.id for row in source.fetch(Cursor(10, 1), 2)] == ["b"]


def test_delete_tombstone_prevents_stale_resurrection():
    store = Store()
    store.apply(event("delete", revision=3, kind="delete"))
    assert not store.apply(event("old", revision=2))
    assert store.records() == {}
    assert store.entry("r").revision == 3


def test_newer_revisions_replace_older_values():
    store = Store()
    store.apply(event("a", revision=1))
    assert store.apply(event("b", revision=2))
    assert store.records()["r"] == {"v": 2}


def test_failed_batch_restores_checkpoint_records_and_seen_ids():
    app = Synchronizer(EventSource([event("a", sequence=1), event("b", sequence=2)]), Store(), 2)
    before = app.store.snapshot()
    with pytest.raises(ApplyFailure):
        app.step(fail_event="b")
    assert app.store.snapshot() == before
    assert app.step().consumed == 2


def test_duplicate_event_id_does_not_apply_twice():
    store = Store()
    row = event("a")
    assert store.apply(row)
    assert not store.apply(row)
    assert store.counts()["seen"] == 1


def test_fetch_failure_changes_nothing():
    app = Synchronizer(EventSource([event("a")]), Store())
    before = app.store.snapshot()
    app.source.fail_next()
    with pytest.raises(FetchFailure):
        app.step()
    assert app.store.snapshot() == before


def test_empty_stream_and_independent_snapshots():
    app = Synchronizer(EventSource([]), Store())
    assert app.run().consumed == 0
    snapshot = app.store.snapshot()
    snapshot.seen.add("changed")
    assert not app.store.seen("changed")


def test_invalid_batch_size_and_duplicate_cursors_are_errors():
    with pytest.raises(ValueError):
        Synchronizer(EventSource([]), Store(), 0)
    with pytest.raises(ValueError):
        EventSource([event("a"), event("b")])


def test_fixture_incremental_run_end_to_end():
    app = synchronizer_from_file(Path(__file__).resolve().parents[1] / "fixtures/events.json", 1)
    result = app.run()
    assert result.consumed == 4
    assert app.store.records() == {"b": {"v": 1}}
    assert report(app)["deleted"] == ["a"]
    assert app.run().consumed == 0
