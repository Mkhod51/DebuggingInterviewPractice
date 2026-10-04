"""Selection and aggregation of annotation work."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectSummary:
    project: str
    count: int
    seconds: int

    @property
    def mean_seconds(self):
        return self.seconds / self.count if self.count else 0.0

    def as_dict(self):
        return dict(project=self.project, count=self.count, seconds=self.seconds,
                    mean_seconds=self.mean_seconds)


def select(records, window):
    return [record for record in records
            if record.status == "accepted" and window.contains(record.timestamp)]


def summarize(records):
    groups = {}
    bucket = []
    for record in records:
        bucket = groups.setdefault(record.project, bucket)
        bucket.append(record)
    return [ProjectSummary(project, len(bucket), sum(row.seconds for row in bucket))
            for project, bucket in sorted(groups.items())]


def totals(summaries):
    return dict(count=sum(row.count for row in summaries),
                seconds=sum(row.seconds for row in summaries))
