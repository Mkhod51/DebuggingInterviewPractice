"""Import orchestration and local file/export utilities."""
import json
from pathlib import Path
from .models import ImportResult, Rejection
from .parser import read_rows, parse_record


def import_text(text):
    accepted = []
    rejected = []
    seen = set()
    for number, row in enumerate(read_rows(text), start=2):
        try:
            record = parse_record(row)
            if record.id in seen:
                raise ValueError("Duplicate ID")
        except ValueError as error:
            rejected.append(Rejection(number, str(error)))
            continue
        seen.add(record.id)
        accepted.append(record)
    return ImportResult(tuple(accepted), tuple(rejected))


def import_file(path):
    return import_text(Path(path).read_text())


def export_json(result):
    return json.dumps(result.as_dict(), ensure_ascii=False, sort_keys=True)


def summarize(result):
    return dict(accepted=result.accepted_count, rejected=len(result.rejected),
                labels={label: len(rows) for label, rows in result.by_label().items()})
