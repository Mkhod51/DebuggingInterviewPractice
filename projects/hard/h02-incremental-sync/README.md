# H02: Incremental sync

## Scenario

A downstream dataset needs to stay up to date with changes made elsewhere.
Instead of copying the whole dataset on every run, it receives a stream of
events saying that individual records were created, updated or deleted. The
stream can repeat events, carry an older record version, or stop during a batch.
The downstream copy must still represent the newest valid state.

This application reads the stream in batches, applies changes to a local store,
and saves how far it has progressed so it can resume. Both source and store are
in-memory exercise components. No external database or streaming platform is
required, and failures can be injected at specific events.

## What the terms mean

- **Record ID:** the identity of the dataset item being changed. Several events
  can affect the same record.
- **Event ID:** the identity of one change notification. Seeing that same event
  again must not apply the change twice.
- **Upsert:** create a record if absent, or replace its value with a newer version.
  A delete event removes its live value.
- **Revision:** a version number for a particular record. Larger revisions are
  newer, even if an older update is delivered later in the stream.
- **Cursor `(timestamp, sequence)`:** an event's position in stream order. The
  sequence distinguishes events with the same timestamp; this is separate from
  the record's revision.
- **Checkpoint:** the last consumed cursor saved by the synchronizer. The next
  fetch starts strictly after it.
- **Tombstone:** a stored deletion marker retaining the record's revision after
  its live value is removed, so an older update cannot undo the deletion.
- **Consumed versus applied:** an event can be read and checkpointed without
  changing a record, for example when it is a duplicate or an old revision.
- **Atomic batch:** record changes, remembered event IDs and checkpoint progress
  are all saved together, or all restored if applying that batch fails.

## Example of correct behavior

Starting from an empty store, the source has these distinct events for record `r`:

| Event ID | Cursor | Revision | Kind | Payload |
| --- | --- | --- | --- | --- |
| e1 | (10, 1) | 1 | upsert | `{"text": "first"}` |
| e2 | (10, 2) | 2 | upsert | `{"text": "edited"}` |
| e3 | (10, 3) | 3 | delete | none |

With batch size 2, the first batch stores `edited` at revision 2 and checkpoint
`(10, 2)`. The next batch deletes the live record, retains a revision-3 tombstone,
and advances to `(10, 3)`. All three events have been consumed and applied. A
second run with no new events consumes zero. If the first batch fails at `e2`,
the store and checkpoint should return to their pre-batch values so it can be
retried in full. This describes required behavior, not current starter output.

## Behavior contract

- Stream order is the composite cursor `(timestamp, sequence)`; both are nonnegative integers and
  each cursor is unique. Events with equal timestamps must all be consumed.
- Fetch events strictly after the saved cursor, in cursor order, up to a positive batch_size.
- Event IDs are stable deduplication keys; duplicate event IDs may appear at later cursors and do not apply again.
- Per-record revisions increase monotonically. A revision no newer than the stored revision is ignored.
- Deletions retain a tombstone revision, so old updates cannot resurrect deleted data. Newer updates can.
- A batch atomically changes records, deduplication IDs and checkpoint. Any injected application failure
  restores all three; retry must process the entire failed batch. Fetch failures change nothing.
- Checkpoint advances to the final consumed event even for duplicates and stale revisions.
- Runs stop on an empty page. Returned snapshots and payloads are independent copies.

## Incident

Resumed syncs miss records sharing a timestamp. Deleted records return, and retries after an interrupted batch sometimes skip unprocessed events.

## Start here

### Codebase map

All application modules are under `src/practice_app/`:

| File | Responsibility |
| --- | --- |
| `models.py` | Cursors, events, stored versions and batch result values. |
| `source.py` | Ordered local event pages and controlled fetch failures. |
| `store.py` | Record versions, seen event IDs, checkpoints and snapshots. |
| `synchronizer.py` | Batch application, recovery and repeated fetches. |
| `audit.py` | Progress counts, record revisions and deleted-record views. |
| `service.py` | Fixture assembly and exported sync reports. |
| `tests/test_sync.py` | Version, resume, duplicate and failure behavior. |
| `fixtures/events.json` | A local sequence of dataset changes. |

The public entry point is `practice_app.synchronizer.Synchronizer.run`. Explore the modules and local fixtures
as needed. No network is used by this application or its tests. Tested on Python
3.14.0; metadata allows Python 3.11+, which has not been separately verified.
Practice session target: 60 minutes (our design choice).

From this project directory, including a standalone copy:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
python -m pytest -q
python -m pytest -q tests/test_sync.py::test_same_timestamp_events_remain_after_checkpoint
```

Installation may download pytest and build tools. Starting application test failures
are intentional. Installation, imports and test discovery must work.

Diagnose and correct application behavior, add regression tests and explain your
evidence and findings. You may add tests. Existing tests and expected outputs are
the contract: do not delete, skip, xfail or weaken them to obtain a pass. A passing
suite is evidence, not proof of correctness for every possible input.
