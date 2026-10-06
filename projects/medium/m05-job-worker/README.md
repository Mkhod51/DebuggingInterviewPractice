# M05: Retrying job worker

## Scenario

A data pipeline has background jobs waiting to be processed, such as importing
a dataset batch. Processing a job can succeed, fail temporarily, or fail in a
way that trying again will not help. The operations team needs the worker to
retry only appropriate failures, respect a finite attempt budget, and retain
an accurate final status and result for each job.

Unlike a queue that only hands work over, this application also calls the job
handler and records the outcome. The handler is a local fake with scripted
outcomes. A controlled clock represents time; the worker does not run a real
background loop or sleep until a retry is due.

## What the terms mean

- **Job:** a uniquely identified payload plus its lifecycle state, attempt count,
  due time, result and latest error.
- **Handler:** the component that tries to perform the job's work. Its scripted
  outcomes let tests reproduce success and failures deterministically.
- **Tick:** one call to `Worker.tick`, which processes the jobs ready at that
  point in time. A job is attempted at most once within that tick.
- **Claim / running:** recording that the worker is starting one attempt. Each
  claim increases the job's attempt count once.
- **Temporary failure / `retry_wait`:** the work may succeed later, so the job is
  scheduled for another attempt if its budget permits.
- **Permanent failure:** retrying is inappropriate; the job becomes failed.
- **Backoff:** increasing the delay between retries. Here it doubles after each
  unsuccessful attempt, starting with `base_delay`.
- **Terminal state:** `succeeded` or `failed`; the worker must not attempt it again.

## Example of correct behavior

A job is ready at time 100, with `max_attempts=3` and `base_delay=2`. Its scripted
handler outcomes are temporary failure, temporary failure, then success. The
first tick records attempt 1 and schedules the retry for time 102. A tick at
101 does nothing for this job. At 102, attempt 2 fails and schedules time 106.
At 106, attempt 3 succeeds and stores the result.

Later ticks leave that succeeded job untouched. If attempt 3 had failed
temporarily, the budget would be exhausted and the job would become failed.
A permanent failure would end processing on the attempt that encountered it.
This timeline describes the intended worker behavior.

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

### Codebase map

All application modules are under `src/practice_app/`:

| File | Responsibility |
| --- | --- |
| `models.py` | Job fields, retry policy and controlled clock. |
| `repository.py` | Stored job state, claims, readiness and independent snapshots. |
| `handler.py` | Scripted successes, temporary errors and permanent errors. |
| `worker.py` | One tick's execution and outcome transitions. |
| `service.py` | Fixture assembly and job state export. |
| `tests/test_worker.py` | Attempt budgets, retry timing and lifecycle examples. |
| `fixtures/jobs.json` | Jobs, clock settings and handler outcomes for a local run. |

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
