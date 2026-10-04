# E04: Contributor directory

A contributor directory supports exact identifier lookup, normalized email search and display profiles with optional quality values.

## Behavior contract

- Contributor IDs are opaque, case-sensitive strings; `A` and `a` are distinct.
- Email search strips outer whitespace and ignores case. Duplicate normalized emails are errors.
- Quality is optional: None means unknown and uses the supplied display default; zero is a real quality value.
- Quality values and display defaults lie in `[0, 1]`; capacity is nonnegative.
- Missing lookups return None. Search returns active profiles only, sorted by exact ID.
- Returned profile dictionaries are independent. Directory creation rejects duplicate exact IDs.

## Incident

Profiles with similar capitalization disappear or collide, and contributors with a recorded zero quality score receive the unknown-score display value.

## Start here

The public entry point is `practice_app.service.DirectoryService.profile`. Explore the modules and local fixtures
as needed. No network is used by this application or its tests. Tested on Python
3.14.0; metadata allows Python 3.11+, which has not been separately verified.
Practice session target: 20–30 minutes (our design choice).

From this project directory, including a standalone copy:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
python -m pytest -q
python -m pytest -q tests/test_directory.py::test_identifiers_are_case_sensitive
```

Installation may download pytest and build tools. Starting application test failures
are intentional. Installation, imports and test discovery must work.

Diagnose and correct application behavior, add regression tests and explain your
evidence and findings. You may add tests. Existing tests and expected outputs are
the contract: do not delete, skip, xfail or weaken them to obtain a pass. A passing
suite is evidence, not proof of correctness for every possible input.
