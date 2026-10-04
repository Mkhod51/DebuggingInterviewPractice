from pathlib import Path
import pytest
from practice_app.models import Review
from practice_app.scoring import summarize
from practice_app.service import generate_report, report_from_file


def test_weighted_mean_uses_total_weight():
    summary = summarize([Review("a", "c", 0, 1), Review("b", "c", 1, 3)])
    assert summary.mean == pytest.approx(0.75)
    assert summary.total_weight == 4


def test_empty_summary_has_no_mean():
    assert summarize([]).as_dict() == {"count": 0, "total_weight": 0, "mean": None}


def test_equal_weight_zero_scores_participate():
    assert summarize([Review("a", "c", 0), Review("b", "c", 1)]).mean == 0.5


def test_invalid_numbers_are_rejected():
    for score, weight in [(float("nan"), 1), (1.1, 1), (0.5, 0), (0.5, float("inf"))]:
        with pytest.raises(ValueError):
            Review("a", "c", score, weight)


def test_duplicate_reviews_are_rejected():
    row = Review("a", "c", 1)
    with pytest.raises(ValueError):
        generate_report([row, row])


def test_contributor_order_and_histogram():
    report = generate_report([Review("a", "z", 0.2), Review("b", "a", 0.95)])
    assert [id for id, summary in report.contributors] == ["a", "z"]
    assert dict(report.score_histogram) == {"low": 1, "middle": 0, "high": 1}


def test_fixture_report_end_to_end():
    report = report_from_file(Path(__file__).resolve().parents[1] / "fixtures/reviews.json")
    assert report.overall.mean == pytest.approx(0.7)
    assert report.as_dict()["contributors"]["a"]["mean"] == 0.7
