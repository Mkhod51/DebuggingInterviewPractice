# H04: Model gateway

## Scenario

Several customer accounts share a text-processing service. Each account has a
default model, a list of models it is allowed to use, and possibly a backup model
for temporary outages. Callers send their requests to a gateway, which chooses
an authorized model, makes the call, checks the response and returns an outcome
with a trace of what happened.

This exercise implements that gateway across several layers. The model transport
is a scripted local fake, so an outage or malformed response can be reproduced
without contacting a real provider. You are debugging request handling and
reliability; no model training or external account setup is involved.

## What the terms mean

- **Tenant:** the customer/account identity used to look up routing permissions.
  It is different from the unique ID of an individual request.
- **Request ID / correlation:** a value identifying the same request through
  routing, transport, retries and response validation. Responses echo it so the
  gateway can check that they belong to the request it sent.
- **Route:** a tenant's default model, allowed model set and optional fallback.
  A caller can explicitly choose a model if it is allowed.
- **Transport:** the component that sends an encoded request to a selected model
  and returns its response. Here it runs entirely locally.
- **Transient failure:** a temporary transport problem for which another attempt
  may help. A permanent failure must end the request immediately.
- **Attempt budget:** `max_attempts` calls per model, including its first call.
- **Fallback:** a different configured model tried after the initial model
  exhausts its transient-failure budget.
- **Protocol validation:** checking response ID, model and output shape before
  trusting the result. An empty string is a valid output; malformed data is not.
- **Trace:** events describing this request's route and execution, all carrying
  its original request ID.

## Example of correct behavior

Tenant `team-a` allows models `primary` and `backup`, defaults to `primary`, and
uses `backup` as fallback. A request `req-42` omits the model selection. With
`max_attempts=2`, suppose the primary fails temporarily twice and the backup
succeeds on its first call. The transport call sequence should be `primary`,
`primary`, `backup`.

The final successful result identifies `backup` as the model and retains request
ID `req-42`; every event in its trace has that same ID. An unauthorized explicit
model selection should instead return an error with no transport calls. A
permanent error from the primary should end after one call. These describe the
gateway's intended external behavior rather than its current implementation.

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

### Codebase map

All application modules are under `src/practice_app/`:

| File | Responsibility |
| --- | --- |
| `models.py` | Incoming requests and final result values. |
| `routing.py` | Tenant permissions and model selection. |
| `protocol.py` | Transport encoding and response validation. |
| `transport.py` | Scripted model responses, failures and recorded calls. |
| `executor.py` | Model attempts and fallback execution. |
| `tracing.py` | Request-owned trace events and operational views. |
| `service.py` | Public request handling and fixture assembly. |
| `tests/test_gateway.py` | Routing, response, failure and trace examples. |
| `fixtures/gateway.json` | Tenant routes, scripted outcomes and sample requests. |

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
