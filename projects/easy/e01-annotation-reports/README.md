# E01: Annotation reports

An operations team generates per-project summaries of accepted annotation work for a reporting window.

## Behavior contract

- Report windows are `[start, end)`, in integer UTC seconds; start must be less than end.
- Include only status `accepted`. Preserve project identifiers exactly.
- Emit one row per included project, sorted by project ID. Count items and sum seconds.
- Empty windows produce no rows; totals count only included annotations.
- IDs must be unique; durations are nonnegative; status is accepted, pending or rejected.
- Inputs are not modified. JSON fixtures and in-memory records use the same validation.

## Incident

Weekly totals omit work recorded exactly when the window begins, and some project summaries appear to inherit another project’s durations.

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
python -m pytest -q tests/test_reports.py::test_report_window_includes_start_and_excludes_end
```

Installation may download pytest and build tools. Starting application test failures
are intentional. Installation, imports and test discovery must work.

Diagnose and correct application behavior, add regression tests and explain your
evidence and findings. You may add tests. Existing tests and expected outputs are
the contract: do not delete, skip, xfail or weaken them to obtain a pass. A passing
suite is evidence, not proof of correctness for every possible input.
