# E01: Annotation reports

## Scenario

An annotation team labels data, such as assigning categories to text. Each completed
piece of work is recorded against a project and later marked accepted, pending or
rejected. An operations person needs a report showing how much accepted work each
project produced during a particular period.

This application takes those records and a time window, then returns one summary
per included project plus overall totals. The report is a Python object that can
also be exported as JSON. You are working on the reporting backend; there is no
dashboard or external service to run.

## What the terms mean

- **Annotation:** one recorded piece of labeling work, identified by `id`.
- **Project:** the group that work belongs to, identified by `project`.
- **Status:** whether the work has been accepted, is awaiting a decision, or was
  rejected. Only accepted work contributes to this report.
- **Timestamp:** when the work was recorded, in integer UTC seconds. This determines
  which reporting window it belongs to.
- **Seconds:** the duration of the work. This is the value to sum, rather than the
  timestamp.
- **Reporting window `[start, end)`:** a period including its start and excluding
  its end, so adjacent reports do not count the same boundary record twice.

## Example of correct behavior

For the window `start=10, end=20`, consider:

| ID | Project | Status | Timestamp | Seconds |
| --- | --- | --- | --- | --- |
| a | alpha | accepted | 12 | 20 |
| b | beta | accepted | 15 | 30 |
| c | alpha | pending | 16 | 8 |

The report should contain `alpha` with count 1 and 20 seconds, then `beta` with
count 1 and 30 seconds. Overall totals are count 2 and 50 seconds. Record `c` is
inside the window but has not been accepted. The original records remain available
unchanged for later reports. This example describes the required result; the
starter implementation may produce a different result.

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

### Codebase map

All application modules are under `src/practice_app/`:

| File | Responsibility |
| --- | --- |
| `models.py` | Annotation records, window validation and fixture loading. |
| `reporting.py` | Record selection, project summaries and overall totals. |
| `service.py` | Report generation, project lookup and JSON export. |
| `tests/test_reports.py` | Executable examples of the required report behavior. |
| `fixtures/annotations.json` | A small local set of annotation records. |

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
