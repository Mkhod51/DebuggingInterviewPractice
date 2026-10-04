"""Request orchestration and report construction."""
from dataclasses import dataclass
from .models import load_input
from .repository import Repository
from .rules import candidates, explain_candidates


@dataclass(frozen=True)
class BatchResult:
    assignments: tuple
    unassigned: tuple

    def as_dict(self):
        return dict(assignments=[row.as_dict() for row in self.assignments],
                    unassigned=list(self.unassigned))


class AssignmentService:
    def __init__(self, repository):
        self.repository = repository

    def assign(self, tasks):
        tasks = list(tasks)
        ids = [task.id for task in tasks]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate task ID in batch")
        assigned = []
        unassigned = []
        for task in tasks:
            existing = self.repository.assignment(task.id)
            if existing is not None:
                assigned.append(existing)
                continue
            available = candidates(self.repository, task)
            if not available:
                unassigned.append(task.id)
                continue
            assigned.append(self.repository.record(task, available[0]))
        return BatchResult(tuple(assigned), tuple(unassigned))

    def explain(self, task):
        return explain_candidates(self.repository, task)

    def release(self, task_id):
        return self.repository.release(task_id)

    def summary(self):
        return self.repository.summary()


def service_from_file(path):
    contributors, tasks = load_input(path)
    return AssignmentService(Repository(contributors)), tasks
