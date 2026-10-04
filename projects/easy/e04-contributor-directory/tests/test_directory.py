from pathlib import Path
import pytest
from practice_app.models import Contributor
from practice_app.directory import Directory
from practice_app.service import DirectoryService, display_quality, service_from_file


def row(id="a", quality=0.8, email="a@example.test"):
    return Contributor(id, "Alex", email, quality)


def test_identifiers_are_case_sensitive():
    directory = Directory([row("A"), row("a", email="other@example.test")])
    assert directory.get("A").email == "a@example.test"
    assert directory.get("a").email == "other@example.test"


def test_zero_quality_is_known():
    assert display_quality(row(quality=0.0), 0.5) == 0.0


def test_missing_quality_uses_default():
    assert display_quality(row(quality=None), 0.5) == 0.5


def test_email_lookup_normalizes_case_and_whitespace():
    assert Directory([row()]).find_email(" A@EXAMPLE.TEST ").id == "a"


def test_unknown_profile_and_independent_rendering():
    service = DirectoryService(Directory([row()]))
    assert service.profile("missing") is None
    profile = service.profile("a")
    profile["name"] = "edited"
    assert service.profile("a")["name"] == "Alex"


def test_duplicate_emails_are_rejected():
    with pytest.raises(ValueError):
        Directory([row("a"), row("b", email=" A@EXAMPLE.TEST ")])


def test_fixture_directory_end_to_end():
    service = service_from_file(Path(__file__).resolve().parents[1] / "fixtures/directory.json")
    assert service.profile("C01")["display_quality"] == 0
    assert service.by_email(" TWO@EXAMPLE.TEST ")["quality_known"] is False
    assert [profile["id"] for profile in service.search("alex")] == ["C01"]
