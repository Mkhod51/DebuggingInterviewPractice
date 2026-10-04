# M04: Prediction cache

A prediction service caches local model responses so repeated identical requests avoid recomputation while preserving model configuration and caller isolation.

## Behavior contract

- Request identity includes model name, version, exact text and JSON options; option key order is irrelevant.
- Cache TTL is positive. A value is valid only while `now < stored_at + ttl`; equality means expired.
- Cache hits must return independent nested response data. Input options and stored values cannot be mutated by callers.
- Expired entries are evicted on lookup. Model-specific invalidation removes only that model’s entries.
- Errors are not cached. Stats count hits, misses and backend calls per service instance.
- Clock time is explicit and monotonic. Responses are JSON-compatible local dictionaries.

## Incident

Changing model configuration still returns a previous prediction. Caller edits to a response appear in later requests, and an expired result occasionally survives its deadline.

## Start here

The public entry point is `practice_app.service.PredictionService.predict`. Explore the modules and local fixtures
as needed. No network is used by this application or its tests. Tested on Python
3.14.0; metadata allows Python 3.11+, which has not been separately verified.
Practice session target: 35–45 minutes (our design choice).

From this project directory, including a standalone copy:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
python -m pytest -q
python -m pytest -q tests/test_cache.py::test_configuration_is_part_of_request_identity
```

Installation may download pytest and build tools. Starting application test failures
are intentional. Installation, imports and test discovery must work.

Diagnose and correct application behavior, add regression tests and explain your
evidence and findings. You may add tests. Existing tests and expected outputs are
the contract: do not delete, skip, xfail or weaken them to obtain a pass. A passing
suite is evidence, not proof of correctness for every possible input.
