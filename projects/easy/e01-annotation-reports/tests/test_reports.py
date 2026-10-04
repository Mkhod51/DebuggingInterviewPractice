from pathlib import Path
import json
import pytest
from practice_app.models import Annotation, Window
from practice_app.reporting import summarize
from practice_app.service import generate_report, report_from_file

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures/annotations.json"


def test_report_window_includes_start_and_excludes_end():
    rows = [Annotation(str(t), "alpha", "accepted", t, 3) for t in [9, 10, 19, 20]]
    assert generate_report(rows, 10, 20).as_dict()["totals"] == {"count": 2, "seconds": 6}


def test_projects_keep_independent_durations():
    rows = [Annotation("a", "alpha", "accepted", 12, 2),
            Annotation("b", "beta", "accepted", 12, 9)]
    assert [(x.project, x.count, x.seconds) for x in summarize(rows)] == [("alpha", 1, 2), ("beta", 1, 9)]


def test_pending_and_rejected_work_is_excluded():
    rows = [Annotation("a", "p", "pending", 12, 2), Annotation("b", "p", "rejected", 12, 7)]
    assert generate_report(rows, 10, 20).rows == ()


def test_empty_report_is_exportable():
    assert json.loads(generate_report([], 1, 2).to_json())["totals"]["count"] == 0


def test_invalid_window_is_rejected():
    with pytest.raises(ValueError):
        Window(2, 2)


def test_duplicate_ids_are_rejected():
    row = Annotation("a", "p", "accepted", 12, 2)
    with pytest.raises(ValueError):
        generate_report([row, row], 10, 20)


def test_fixture_report_end_to_end():
    report = report_from_file(FIXTURE, 10, 20)
    assert report.as_dict()["totals"] == {"count": 3, "seconds": 13}
    assert report.for_project("beta").seconds == 7
    assert report.for_project("missing") is None
