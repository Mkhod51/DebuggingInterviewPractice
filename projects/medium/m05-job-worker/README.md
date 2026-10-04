# M05: Retrying job worker

A local worker processes queued dataset jobs, retries temporary failures on a controlled clock and records terminal outcomes.

## Behavior contract

- Jobs start queued with attempts zero. A claim increments attempts exactly once and sets running.
- Ready queued or retry_wait jobs have due_at <= now; process by due_at then ID. Each tick snapshots
  ready IDs, so a job is attempted at most once per tick, even if the clock is advanced later.
- max_attempts includes the initial call. A temporary failure retries only while attempts < max_attempts.
- Retry delay after attempt n is base_delay * 2**(n-1), relative to the current failure time.
- Permanent and unexpected handler errors become terminal failed immediately. Only temporary errors retry.
- Success records independent result data, clears the error and becomes terminal succeeded.
- Terminal jobs are never claimed again. Job IDs are unique; snapshots cannot mutate repository state.
- Clock and fake handler are local; no real waits or network are used.

## Incident

Some jobs exceed their attempt budget, permanent errors are retried, and retries scheduled later in the day become ready immediately.

## Start here

The public entry point is `practice_app.worker.Worker.tick`. Explore the modules and local fixtures
as needed. No network is used by this application or its tests. Tested on Python
3.14.0; metadata allows Python 3.11+, which has not been separately verified.
Practice session target: 35–45 minutes (our design choice).

From this project directory, including a standalone copy:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
python -m pytest -q
python -m pytest -q tests/test_worker.py::test_retry_budget_includes_first_attempt
```

Installation may download pytest and build tools. Starting application test failures
are intentional. Installation, imports and test discovery must work.

Diagnose and correct application behavior, add regression tests and explain your
evidence and findings. You may add tests. Existing tests and expected outputs are
the contract: do not delete, skip, xfail or weaken them to obtain a pass. A passing
suite is evidence, not proof of correctness for every possible input.
