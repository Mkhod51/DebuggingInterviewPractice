# E05: Quality scores

A quality service combines reviewed annotation scores into weighted contributor summaries and a dataset summary.

## Behavior contract

- Each review has a finite score in `[0, 1]`, positive finite weight and a unique review ID.
- The quality mean is `sum(score * weight) / sum(weight)`; contributor and overall summaries use the same rule.
- Empty inputs have count zero, total weight zero and mean None. Zero scores participate normally.
- Contributors are sorted by exact identifier. Internal means retain floating-point precision;
  JSON exports round means to four decimal places without altering internal results.
- Inputs and prior report objects must not be mutated. Duplicate review IDs are errors.

## Incident

The dashboard disagrees with manual weighted calculations, and a contributor with no reviews causes report generation to fail.

## Start here

The public entry point is `practice_app.service.generate_report`. Explore the modules and local fixtures
as needed. No network is used by this application or its tests. Tested on Python
3.14.0; metadata allows Python 3.11+, which has not been separately verified.
Practice session target: 20–30 minutes (our design choice).

From this project directory, including a standalone copy:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
python -m pytest -q
python -m pytest -q tests/test_scores.py::test_weighted_mean_uses_total_weight
```

Installation may download pytest and build tools. Starting application test failures
are intentional. Installation, imports and test discovery must work.

Diagnose and correct application behavior, add regression tests and explain your
evidence and findings. You may add tests. Existing tests and expected outputs are
the contract: do not delete, skip, xfail or weaken them to obtain a pass. A passing
suite is evidence, not proof of correctness for every possible input.
