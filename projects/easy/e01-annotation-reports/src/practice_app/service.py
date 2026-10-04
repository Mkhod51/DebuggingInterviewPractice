"""Public report API and a JSON export boundary."""
from dataclasses import dataclass
import json
from .models import Window, load_annotations, validate_unique
from .reporting import select, summarize, totals


@dataclass(frozen=True)
class Report:
    window: Window
    rows: tuple

    def as_dict(self):
        return dict(start=self.window.start, end=self.window.end,
                    projects=[row.as_dict() for row in self.rows],
                    totals=totals(self.rows))

    def to_json(self):
        return json.dumps(self.as_dict(), sort_keys=True)

    def for_project(self, project):
        return next((row for row in self.rows if row.project == project), None)


def generate_report(records, start, end):
    records = list(records)
    validate_unique(records)
    window = Window(start, end)
    included = select(records, window)
    return Report(window, tuple(summarize(included)))


def report_from_file(path, start, end):
    return generate_report(load_annotations(path), start, end)
