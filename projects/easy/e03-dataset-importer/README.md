# E03: Dataset importer

A dataset importer reads quoted CSV rows, validates them independently and returns accepted records alongside row-level diagnostics.

## Behavior contract

- Required headers: `id`, `text`, `weight`; an optional `label` header is supported.
- IDs are stripped of outer whitespace but otherwise preserved, including leading zeroes.
- Text is preserved exactly, including commas and newlines inside quoted CSV fields; empty text is invalid.
- Weight is a finite number in `(0, 1]`. Invalid rows are rejected without stopping other rows.
- Duplicate accepted IDs are rejected; a rejected row does not reserve its ID.
- Missing label values become `unlabeled`; explicitly empty labels stay empty.
- Header errors fail the entire import. Diagnostic row numbers count logical records, starting at 2.

## Incident

Imported record identifiers no longer match external references, and text containing quoted line breaks loses formatting.

## Start here

The public entry point is `practice_app.service.import_text`. Explore the modules and local fixtures
as needed. No network is used by this application or its tests. Tested on Python
3.14.0; metadata allows Python 3.11+, which has not been separately verified.
Practice session target: 20–30 minutes (our design choice).

From this project directory, including a standalone copy:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
python -m pytest -q
python -m pytest -q tests/test_importer.py::test_identifiers_preserve_leading_zeroes
```

Installation may download pytest and build tools. Starting application test failures
are intentional. Installation, imports and test discovery must work.

Diagnose and correct application behavior, add regression tests and explain your
evidence and findings. You may add tests. Existing tests and expected outputs are
the contract: do not delete, skip, xfail or weaken them to obtain a pass. A passing
suite is evidence, not proof of correctness for every possible input.
