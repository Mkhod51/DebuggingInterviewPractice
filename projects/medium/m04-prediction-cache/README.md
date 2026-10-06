# M04: Prediction cache

## Scenario

A text-processing service receives repeated requests for model predictions.
Calling the model for every identical request would repeat work, so the service
keeps successful responses in memory for a limited time. A later request can
reuse a saved response only if it represents the same computation and the saved
value has not expired.

This exercise implements that prediction service and cache. The model is a local
fake that returns deterministic dictionaries. Callers can edit returned data,
and the clock is controlled explicitly so expiration can be tested immediately
without waiting in real time.

## What the terms mean

- **Request:** a model name, version, exact input text and JSON options. Options
  represent settings that can change what the model returns.
- **Request identity / cache key:** the description of the computation whose
  saved result may be reused. All request fields above matter to that identity.
- **Backend:** the fake model that produces a response when a saved value cannot
  be used. A backend call is an actual invocation of that model object.
- **Cache hit:** a valid saved response was found. A miss means the service needs
  to call the backend.
- **TTL (time to live):** how long a saved response remains usable from the time
  it is stored. At the expiration time itself, it is no longer valid.
- **Caller isolation:** editing a returned dictionary, including its nested
  values, must not change the data received by another request.
- **Invalidation:** explicitly removing saved responses for a particular model.

## Example of correct behavior

At clock time 100, request model `a`, version `1`, text `hello`, and no options.
With TTL 10, the first request is a miss and calls the backend. An identical
request at time 105 is a hit: after those two requests, stats should show one
miss, one hit and one backend call.

At time 110 the saved response has expired, so the same request calls the backend
again. A request with another version or different options is also a separate
computation. Mutating any returned response must not change a later result.
These examples describe required behavior, not guaranteed starter output.

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

### Codebase map

All application modules are under `src/practice_app/`:

| File | Responsibility |
| --- | --- |
| `models.py` | Request identity, controlled clock and statistics values. |
| `cache.py` | Saved response storage, expiration and invalidation. |
| `backend.py` | Local response generation and controlled model failures. |
| `service.py` | Prediction requests, cache/backend coordination and stats. |
| `tests/test_cache.py` | Repeated requests, time changes and caller data ownership. |
| `fixtures/requests.json` | A local sequence of model requests. |

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
