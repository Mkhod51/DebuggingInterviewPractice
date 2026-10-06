# M02: Paginated dataset client

## Scenario

A data team wants to export all records from a dataset API. The API does not
return the entire dataset in one response: it returns a page of records and a
token for requesting the next page. Records can overlap between pages, so the
export must avoid repeating them while preserving the order in which they first
appeared.

This application is the client that makes those page requests and assembles one
complete export. A local fake API supplies the responses and records the calls;
there is no real HTTP server or network connection. You can inspect exactly what
was requested and returned.

## What the terms mean

- **Dataset:** the named collection requested by the caller.
- **Page:** one API response containing `items` and `next_cursor`. Each item has
  an exact record ID and a dictionary payload.
- **Pagination:** fetching a large collection through a sequence of page requests.
- **Cursor:** an opaque continuation token issued by the API. Opaque means pass
  it back as supplied, without interpreting it as a number or page index.
- **`None`:** as a request cursor, start from the first page; as a response's next
  cursor, there are no more pages. An empty string is a different, valid token.
- **Deduplication:** keeping just the first occurrence of each record ID across
  all pages, including its original payload.
- **Protocol error:** a response or page sequence that breaks the API contract,
  such as a continuation loop. It prevents a supposedly complete export being returned.

## Example of correct behavior

Suppose the first page contains IDs `a, b` and next cursor `"next"`. The response
to cursor `"next"` contains IDs `b, c` and next cursor `None`. The complete export
should have IDs `a, b, c`, in that order, with `page_count=2`. If the two copies of
`b` have different payloads, the one from the first page wins.

The final page's records still belong in the export even though its next cursor
says to stop. An empty page with a continuation token still indicates that there
is another page to request. These describe expected API behavior, rather than
the current output of the buggy starter.

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

### Codebase map

All application modules are under `src/practice_app/`:

| File | Responsibility |
| --- | --- |
| `api.py` | Fake page responses, recorded requests and injected API failures. |
| `models.py` | Page/record shapes and response validation. |
| `pagination.py` | Page traversal, loop guards and record collection. |
| `service.py` | Dataset fetch entry point and export result. |
| `tests/test_client.py` | Scripted page sequences and expected complete exports. |
| `fixtures/pages.json` | Local pages for the `demo` dataset. |

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
