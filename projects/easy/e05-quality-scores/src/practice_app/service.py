"""Public reporting and stable JSON export."""
from dataclasses import dataclass
import json
from .models import load_reviews
from .scoring import by_contributor, summarize, validate_unique, histogram


@dataclass(frozen=True)
class Report:
    overall: object
    contributors: tuple
    score_histogram: tuple

    def as_dict(self):
        return dict(overall=self.overall.as_dict(),
                    contributors={id: summary.as_dict() for id, summary in self.contributors},
                    histogram=dict(self.score_histogram))

    def contributor(self, identifier):
        return next((summary for id, summary in self.contributors if id == identifier), None)

    def to_json(self):
        return json.dumps(self.as_dict(), sort_keys=True)


def generate_report(reviews):
    reviews = list(reviews)
    validate_unique(reviews)
    return Report(summarize(reviews), tuple(by_contributor(reviews).items()),
                  tuple(histogram(reviews).items()))


def report_from_file(path):
    return generate_report(load_reviews(path))
