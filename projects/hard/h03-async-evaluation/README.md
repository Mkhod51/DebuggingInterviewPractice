# H03: Asynchronous evaluation

## Scenario

A team evaluates a text-labeling model on examples with known expected answers.
To finish sooner, the service allows several prediction calls to be in progress
at once. Those calls can finish in a different order from the input examples, and
one call can fail while the others succeed. A user may also cancel the whole run
while predictions are still pending.

Your application coordinates the concurrent calls, produces a report in the
original example order, and owns the cleanup of any unfinished work. The model
is a local fake. Tests explicitly release its calls in chosen orders, so there
is no dependency on model knowledge, real network timing or arbitrary sleeps.

## What the terms mean

- **Case:** an example with a unique ID, input text and expected label.
- **Completion:** the eventual value or error from one prediction call, tagged
  with its case ID. Finishing first does not mean it belongs to the first case.
- **Asynchronous / concurrent:** several calls can be in progress while each
  awaits completion. The caller uses `await` to wait for the evaluation result.
- **`max_concurrency`:** the maximum number of active model calls at any instant,
  rather than a limit on the total number of cases in the run.
- **Child task:** one asynchronous unit of work created for a prediction.
- **Cancellation:** the caller stops waiting for the run. The run must cancel
  its child tasks and wait for their cleanup before propagating `CancelledError`.
- **Accuracy and coverage:** accuracy is correct labels / successful predictions;
  coverage is successful predictions / all input cases. A model error has no
  correctness value and is not an incorrect label.
- **Gate:** a test-controlled signal that lets a fake prediction finish. It
  makes completion order and cleanup observable without real-time delays.

## Example of correct behavior

Input cases are `a`, `b`, `c`; their expected labels are `yes`, `no`, `yes`.
With concurrency 2, no more than two predictions may be active at once. Suppose
`b` finishes before `a`, both return their expected labels, and `c` later fails.
The report should still list `a`, `b`, `c`, with correctness values `True`,
`True`, `None`. Accuracy is 1 and coverage is `2/3`.

If the caller cancels while calls are pending, the run should raise
`CancelledError` only after those child tasks have been cleaned up. The runner
can then be used for another run, with no active work left from the cancelled
one. These are expected lifecycle results to compare with the starter.

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

### Codebase map

All application modules are under `src/practice_app/`:

| File | Responsibility |
| --- | --- |
| `models.py` | Cases, completions, per-case results and fixture loading. |
| `controlled_model.py` | Fake predictions, completion gates and active-call observations. |
| `runner.py` | Concurrent execution, run ownership and cancellation cleanup. |
| `lifecycle.py` | Observable lifecycle stages for a run and its cleanup. |
| `association.py` | Completion identity checks and results in input order. |
| `metrics.py` | Accuracy, coverage and report values. |
| `service.py` | Local orchestration, controlled finish order and fixture evaluation. |
| `tests/test_async.py` | Concurrent execution, failures and cancellation scenarios. |
| `fixtures/evaluation.json` | Cases, outcomes and a controlled completion order. |

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
