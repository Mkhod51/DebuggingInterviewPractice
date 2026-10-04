from pathlib import Path
import pytest
from practice_app.models import Request
from practice_app.routing import Route, Router
from practice_app.protocol import encode, decode, ProtocolError
from practice_app.transport import FakeTransport
from practice_app.executor import Executor
from practice_app.service import Gateway, gateway_from_file


def gateway(scripts=None):
    route = Route("primary", frozenset({"primary", "chosen", "backup"}), "backup")
    return Gateway(Router({"tenant": route}), Executor(FakeTransport(scripts), 2))


def request(model=None, text="hello"):
    return Request("req-1", "tenant", text, model)


def test_request_id_survives_transport_encoding():
    assert encode(request(), "primary")["request_id"] == "req-1"


def test_explicit_allowed_model_overrides_default():
    selection = gateway().router.select(request("chosen"))
    assert selection.primary == "chosen"


def test_permanent_failure_does_not_retry_or_fallback():
    app = gateway({"primary": ["permanent", "success"]})
    result = app.handle(request())
    assert not result.ok and result.error == "Request refused"
    assert [call["model"] for call in app.executor.transport.calls] == ["primary"]


def test_empty_output_is_valid():
    assert decode(request(), "primary", {"request_id": "req-1", "model": "primary", "output": ""}) == ""


def test_unauthorized_or_unknown_tenant_never_contacts_transport():
    app = gateway()
    assert not app.handle(request("forbidden")).ok
    assert not app.handle(Request("x", "unknown", "text")).ok
    assert app.executor.transport.calls == []


def test_response_model_mismatch_is_rejected():
    with pytest.raises(ProtocolError):
        decode(request(), "primary", {"request_id": "req-1", "model": "other", "output": "text"})


def test_invalid_route_and_attempt_budget_are_errors():
    with pytest.raises(ValueError):
        Route("unknown", frozenset({"primary"}))
    with pytest.raises(ValueError):
        Executor(FakeTransport(), 0)


def test_fixture_gateway_end_to_end():
    app, requests = gateway_from_file(Path(__file__).resolve().parents[1] / "fixtures/gateway.json")
    result = app.handle(requests[0])
    assert result.ok and result.output == " olleh " and result.model == "backup"
    assert [call["model"] for call in app.executor.transport.calls] == ["primary", "primary", "backup"]
    assert all(event.request_id == "trace-42" for event in result.trace)
