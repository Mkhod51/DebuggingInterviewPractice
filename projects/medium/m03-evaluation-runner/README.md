# M03: Evaluation runner

A model evaluation runner requests local predictions in batches, associates outputs with examples and reports accuracy separately from operational failures.

## Behavior contract

- Cases have unique exact IDs, input text and expected labels. Predictions may arrive in any order.
- Associate by case ID and preserve original case order in results. Missing outputs become errors.
- Duplicate or unknown output IDs are protocol errors; a run produces no report on protocol failure.
- A prediction can contain either a value or an error, never both. Successful label matching is exact.
- Accuracy is correct / successfully scored cases; failed cases are excluded from that denominator.
- Coverage is scored / total. Empty runs and all-error runs have accuracy None; empty coverage is 0.
- Positive batch_size limits each local model call. No network or real model is involved.

## Incident

Some examples are marked incorrect despite the model returning their expected labels. Accuracy also changes when operational failures are added.

## Start here

The public entry point is `practice_app.service.EvaluationRunner.run`. Explore the modules and local fixtures
as needed. No network is used by this application or its tests. Tested on Python
3.14.0; metadata allows Python 3.11+, which has not been separately verified.
Practice session target: 35–45 minutes (our design choice).

From this project directory, including a standalone copy:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
python -m pytest -q
python -m pytest -q tests/test_evaluation.py::test_out_of_order_predictions_match_their_cases
```

Installation may download pytest and build tools. Starting application test failures
are intentional. Installation, imports and test discovery must work.

Diagnose and correct application behavior, add regression tests and explain your
evidence and findings. You may add tests. Existing tests and expected outputs are
the contract: do not delete, skip, xfail or weaken them to obtain a pass. A passing
suite is evidence, not proof of correctness for every possible input.
