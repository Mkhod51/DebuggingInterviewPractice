from pathlib import Path
import json
import pytest
from practice_app.parser import parse_record, read_rows
from practice_app.service import import_text, import_file, export_json


def test_identifiers_preserve_leading_zeroes():
    result = import_text("id,text,weight\n001,hello,1\n1,world,0.5\n")
    assert [row.id for row in result.records] == ["001", "1"]


def test_quoted_multiline_text_is_preserved():
    result = import_text('id,text,weight\nx,"first\nsecond, line",1\n')
    assert result.records[0].text == "first\nsecond, line"


def test_invalid_rows_do_not_reserve_ids():
    result = import_text("id,text,weight\nx,hello,nan\nx,world,1\n")
    assert result.accepted_count == 1
    assert result.rejected[0].row == 2


def test_missing_and_empty_labels_are_distinct():
    assert parse_record({"id": "x", "text": "t", "weight": "1"}).label == "unlabeled"
    assert parse_record({"id": "x", "text": "t", "weight": "1", "label": ""}).label == ""


def test_missing_or_duplicate_headers_are_errors():
    for text in ["id,text\nx,t\n", "id,text,weight,id\nx,t,1,x\n"]:
        with pytest.raises(ValueError):
            read_rows(text)


def test_duplicate_records_and_invalid_weights_are_rejected():
    result = import_text("id,text,weight\nx,hello,1\nx,again,1\ny,t,0\nz,t,1.1\n")
    assert result.accepted_count == 1
    assert len(result.rejected) == 3


def test_fixture_import_end_to_end():
    result = import_file(Path(__file__).resolve().parents[1] / "fixtures/input.csv")
    exported = json.loads(export_json(result))
    assert exported["records"][0] == {"id": "007", "text": "hello\nworld", "weight": 0.5, "label": ""}
    assert len(result.rejected) == 1
