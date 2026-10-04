# H02: Incremental sync

An incremental synchronizer consumes a local event stream into a versioned dataset, saving checkpoints for safe resumable processing.

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
