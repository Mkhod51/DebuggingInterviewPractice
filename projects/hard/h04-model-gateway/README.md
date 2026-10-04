# H04: Model gateway

A model gateway validates tenant requests, chooses authorized local routes, retries temporary transport failures and emits correlated request traces.

## Behavior contract

- Requests carry exact request_id, tenant, text, optional model and JSON options. Preserve text and IDs exactly.
- Each tenant has a default, allowed model set and optional fallback. An explicit allowed model overrides the default.
- Unknown tenants or unauthorized models return an error without contacting transport.
- Each model gets max_attempts calls, including its first call. Only transient transport failures retry.
- After exhausting transient attempts, try the configured distinct fallback with the same budget.
  Permanent errors and malformed responses terminate immediately, without retry or fallback.
- Responses must echo the request ID and chosen model, and contain a string output. Empty output is valid.
- The final result identifies the model actually contacted and includes only this request’s trace events.
  Every trace event preserves the original request ID, even across retries and fallback.
- Request options, transport calls and response data are independent copies. Everything is local.

## Incident

Requests produce correlation errors, explicit model selection is ignored, permanent failures trigger more calls, and successful empty responses are rejected.

## Start here

The public entry point is `practice_app.service.Gateway.handle`. Explore the modules and local fixtures
as needed. No network is used by this application or its tests. Tested on Python
3.14.0; metadata allows Python 3.11+, which has not been separately verified.
Practice session target: 60 minutes (our design choice).

From this project directory, including a standalone copy:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
python -m pytest -q
python -m pytest -q tests/test_gateway.py::test_request_id_survives_transport_encoding
```

Installation may download pytest and build tools. Starting application test failures
are intentional. Installation, imports and test discovery must work.

Diagnose and correct application behavior, add regression tests and explain your
evidence and findings. You may add tests. Existing tests and expected outputs are
the contract: do not delete, skip, xfail or weaken them to obtain a pass. A passing
suite is evidence, not proof of correctness for every possible input.
