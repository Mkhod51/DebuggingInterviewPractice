"""Qualification checks using a planned state rather than live mutation."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Eligibility:
    allowed: bool
    reasons: tuple


def assess(contributor, task, project, state):
    reasons = []
    if not contributor.active:
        reasons.append("inactive")
    if task.id not in contributor.projects:
        reasons.append("project")
    if not task.certifications.issubset(contributor.certifications):
        reasons.append("certifications")
    if task.language not in contributor.languages:
        reasons.append("language")
    if state.loads[contributor.id] + task.units > contributor.capacity:
        reasons.append("capacity")
    if state.usage[project.id] >= project.quota:
        reasons.append("quota")
    return Eligibility(not reasons, tuple(reasons))


def rank(contributors, task, project, state):
    available = [row for row in contributors if assess(row, task, project, state).allowed]
    return sorted(available, key=lambda row: (state.loads[row.id], row.id))


def explain(contributors, task, project, state):
    return {row.id: assess(row, task, project, state).reasons for row in contributors}
