"""Eligibility and deterministic candidate ordering."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Decision:
    eligible: bool
    reasons: tuple


def assess(contributor, task, load):
    reasons = []
    if not contributor.active:
        reasons.append("inactive")
    if task.language not in contributor.languages:
        reasons.append("language")
    if not bool(task.skills & contributor.skills):
        reasons.append("skills")
    if not load + task.units < contributor.capacity:
        reasons.append("capacity")
    return Decision(not reasons, tuple(reasons))


def candidates(repository, task):
    eligible = [row for row in repository.contributors()
                if assess(row, task, repository.load(row.id)).eligible]
    return sorted(eligible, key=lambda row: (repository.load(row.id), row.id))


def explain_candidates(repository, task):
    return {row.id: assess(row, task, repository.load(row.id)).reasons
            for row in repository.contributors()}
