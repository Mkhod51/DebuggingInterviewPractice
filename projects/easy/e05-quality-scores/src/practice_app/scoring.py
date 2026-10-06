"""Aggregation independent of transport or display formatting."""
from .models import Summary


def summarize(reviews):
    reviews = list(reviews)
    total_weight = sum(row.weight for row in reviews)
    weighted_sum = sum(row.score * row.weight for row in reviews)
    mean = weighted_sum / total_weight if reviews else None
    return Summary(len(reviews), total_weight, mean)


def by_contributor(reviews):
    groups = {}
    for row in reviews:
        groups.setdefault(row.contributor, []).append(row)
    return {identifier: summarize(rows) for identifier, rows in sorted(groups.items())}


def validate_unique(reviews):
    ids = [row.id for row in reviews]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate review ID")


def histogram(reviews):
    result = {"low": 0, "middle": 0, "high": 0}
    for review in reviews:
        bucket = "low" if review.score < 0.5 else "middle" if review.score < 0.9 else "high"
        result[bucket] += 1
    return result
