# M02: Paginated dataset client

A dataset client follows opaque pagination cursors from a local API and returns a stable deduplicated export.

## Behavior contract

- None denotes the first request and, in a response, the end of pagination. Empty-string cursors are valid.
- Fetch every page, including the final page. Preserve page order and item order.
- Deduplicate records by exact ID across pages, keeping the first occurrence.
- Requests identify the dataset and positive page size. Cursor values must not be interpreted numerically.
- Repeated response cursors or exceeding a positive max_pages limit raise ProtocolError; no partial result is returned.
- Malformed responses raise ProtocolError. Fake responses and returned data are independent copies.
- An empty page may still have a next cursor. API exceptions propagate to callers.

## Incident

Exports stop unexpectedly on some cursor values, and multi-page exports contain only the most recent page.

## Start here

The public entry point is `practice_app.service.DatasetClient.fetch`. Explore the modules and local fixtures
as needed. No network is used by this application or its tests. Tested on Python
3.14.0; metadata allows Python 3.11+, which has not been separately verified.
Practice session target: 35–45 minutes (our design choice).

From this project directory, including a standalone copy:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
python -m pytest -q
python -m pytest -q tests/test_client.py::test_empty_string_is_a_valid_next_cursor
```

Installation may download pytest and build tools. Starting application test failures
are intentional. Installation, imports and test discovery must work.

Diagnose and correct application behavior, add regression tests and explain your
evidence and findings. You may add tests. Existing tests and expected outputs are
the contract: do not delete, skip, xfail or weaken them to obtain a pass. A passing
suite is evidence, not proof of correctness for every possible input.
