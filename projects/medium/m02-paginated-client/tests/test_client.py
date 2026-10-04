from pathlib import Path
import pytest
from practice_app.api import FakeAPI
from practice_app.models import ProtocolError, Page
from practice_app.service import DatasetClient, client_from_file


def page(ids, cursor=None):
    return {"items": [{"id": id, "payload": {"text": id}} for id in ids], "next_cursor": cursor}


def test_empty_string_is_a_valid_next_cursor():
    api = FakeAPI({"d": {"__first__": page(["a"], ""), "": page(["b"])}})
    result = DatasetClient(api).fetch("d")
    assert result.page_count == 2
    assert [call.cursor for call in api.calls] == [None, ""]


def test_records_accumulate_and_deduplicate_across_pages():
    api = FakeAPI({"d": {"__first__": page(["a", "b"], "next"), "next": page(["b", "c"])}})
    assert [row.id for row in DatasetClient(api).fetch("d").records] == ["a", "b", "c"]


def test_single_empty_page_is_valid():
    result = DatasetClient(FakeAPI({"d": {"__first__": page([])}})).fetch("d")
    assert result.records == () and result.page_count == 1


def test_repeated_cursor_raises_protocol_error():
    api = FakeAPI({"d": {"__first__": page([], "x"), "x": page([], "x")}})
    with pytest.raises(ProtocolError):
        DatasetClient(api).fetch("d")


def test_response_and_request_validation():
    with pytest.raises(ProtocolError):
        Page.from_dict({"items": [], "next_cursor": 0})
    with pytest.raises(ValueError):
        DatasetClient(FakeAPI({})).fetch("d", page_size=0)


def test_fake_api_returns_independent_copies_and_propagates_errors():
    api = FakeAPI({"d": {"__first__": page(["a"])}})
    response = api.fetch_page("d", None, 5)
    response["items"].clear()
    assert len(api.fetch_page("d", None, 5)["items"]) == 1
    api.calls.clear()
    assert len(api.calls) == 2
    with pytest.raises(KeyError):
        api.fetch_page("missing", None, 5)


def test_fixture_export_end_to_end():
    client = client_from_file(Path(__file__).resolve().parents[1] / "fixtures/pages.json")
    result = client.fetch("demo", page_size=2)
    assert [row.id for row in result.records] == ["a", "b", "c"]
    assert result.find("a")["payload"] == {"text": "first"}
    assert result.page_count == 3
