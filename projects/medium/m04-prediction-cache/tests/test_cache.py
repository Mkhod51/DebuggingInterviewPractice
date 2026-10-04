from pathlib import Path
import pytest
from practice_app.models import Request, Clock
from practice_app.cache import Cache
from practice_app.backend import FakeModel, ModelError
from practice_app.service import PredictionService, service_from_file


def service():
    clock = Clock()
    return PredictionService(FakeModel(), Cache(clock, 10)), clock


def test_configuration_is_part_of_request_identity():
    app, clock = service()
    first = app.predict("a", "1", "hello", {"temperature": 0})
    second = app.predict("b", "2", "hello", {"temperature": 1})
    assert second["model"] == "b" and second["version"] == "2"
    assert second["options"] == {"temperature": 1}
    assert app.stats().backend_calls == 2


def test_hit_results_do_not_share_nested_state():
    app, clock = service()
    app.predict("a", "1", "hello world")
    hit = app.predict("a", "1", "hello world")
    hit["details"]["tokens"].append("edited")
    assert app.predict("a", "1", "hello world")["details"]["tokens"] == ["hello", "world"]


def test_deadline_is_expired():
    app, clock = service()
    app.predict("a", "1", "hello")
    clock.advance(10)
    app.predict("a", "1", "hello")
    assert app.stats().backend_calls == 2


def test_option_key_order_does_not_change_identity():
    assert Request("a", "1", "t", {"x": 1, "y": 2}).key() == Request("a", "1", "t", {"y": 2, "x": 1}).key()


def test_errors_are_not_cached():
    app, clock = service()
    app.backend.fail_next()
    with pytest.raises(ModelError):
        app.predict("a", "1", "hello")
    assert app.predict("a", "1", "hello")["prediction"] == "HELLO"
    assert app.stats().backend_calls == 2


def test_miss_returns_caller_owned_result():
    app, clock = service()
    first = app.predict("a", "1", "hello")
    first["details"]["tokens"].clear()
    assert app.predict("a", "1", "hello")["details"]["tokens"] == ["hello"]


def test_invalid_ttl_and_backwards_clock_are_errors():
    with pytest.raises(ValueError):
        Cache(Clock(), 0)
    with pytest.raises(ValueError):
        Clock().advance(-1)


def test_fixture_service_end_to_end():
    app, clock, requests = service_from_file(Path(__file__).resolve().parents[1] / "fixtures/requests.json")
    responses = [app.predict(**request) for request in requests]
    assert [row["model"] for row in responses] == ["a", "a", "b"]
    assert app.stats().as_dict() == {"hits": 1, "misses": 2, "backend_calls": 2}
