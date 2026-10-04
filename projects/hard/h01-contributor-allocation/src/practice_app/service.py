"""Allocation entry points coordinating plans, publication and auditing."""
from dataclasses import dataclass
from .audit import inspect
from .eligibility import explain
from .models import load_input
from .planner import build_plan, validate_tasks
from .repository import Repository


@dataclass(frozen=True)
class RunResult:
    plan: object
    audit: object

    def as_dict(self):
        return dict(plan=self.plan.as_dict(), audit=self.audit.as_dict())


class AllocationService:
    def __init__(self, repository):
        self.repository = repository

    def _plan(self, tasks):
        tasks = list(tasks)
        validate_tasks(tasks, self.repository.projects)
        snapshot = self.repository.snapshot()
        pending = [task for task in tasks if task.project not in snapshot.assignments]
        return build_plan(list(self.repository.contributors.values()),
                          self.repository.projects, pending, snapshot)

    def preview(self, tasks):
        return self._plan(tasks)

    def run(self, tasks, fail_task=None):
        plan = self._plan(tasks)
        self.repository.commit(plan, fail_task=fail_task)
        return RunResult(plan, inspect(self.repository))

    def explain(self, task):
        return explain(list(self.repository.contributors.values()), task,
                       self.repository.projects[task.project], self.repository.snapshot())

    def release(self, task_id):
        return self.repository.release(task_id)

    def audit(self):
        return inspect(self.repository)


def service_from_file(path):
    contributors, projects, tasks = load_input(path)
    return AllocationService(Repository(contributors, projects)), tasks
