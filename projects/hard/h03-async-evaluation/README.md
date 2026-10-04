# H03: Asynchronous evaluation

An asynchronous evaluation service runs local predictions concurrently, records per-case failures and cleans up work when its caller cancels.

## Behavior contract

- Each input ID is unique. Completion order is arbitrary; output order must match input order and associate by ID.
- At most max_concurrency model calls may be active. The limit is positive; a runner rejects overlapping runs.
- Ordinary model errors affect only that case: actual and correct are None and error is recorded.
- Successful predictions are compared exactly with expected labels. Accuracy excludes errors; coverage includes them.
- Empty input produces an empty report with accuracy None and coverage zero.
- Caller cancellation propagates CancelledError and cancels and awaits every child task before the run finishes.
- After either success or cancellation the runner is reusable, with no active child tasks.
- Fake clients use explicit event gates and queues. Tests control completion order without sleeps or timeouts.

## Incident

Results follow completion order rather than example identity. Failed calls appear scored, concurrency exceeds the configured limit, and cancelled runs continue doing work.

## Start here

The public entry point is `practice_app.runner.AsyncRunner.run`. Explore the modules and local fixtures
as needed. No network is used by this application or its tests. Tested on Python
3.14.0; metadata allows Python 3.11+, which has not been separately verified.
Practice session target: 60 minutes (our design choice).

From this project directory, including a standalone copy:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
python -m pytest -q
python -m pytest -q tests/test_async.py::test_completion_order_does_not_change_result_identity
```

Installation may download pytest and build tools. Starting application test failures
are intentional. Installation, imports and test discovery must work.

Diagnose and correct application behavior, add regression tests and explain your
evidence and findings. You may add tests. Existing tests and expected outputs are
the contract: do not delete, skip, xfail or weaken them to obtain a pass. A passing
suite is evidence, not proof of correctness for every possible input.
