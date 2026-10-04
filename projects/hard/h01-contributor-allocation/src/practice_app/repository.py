"""Local storage with atomic publication of an allocation plan."""
from .models import State


class CommitFailure(RuntimeError):
    """Controlled storage failure used by local callers."""


class Repository:
    def __init__(self, contributors, projects):
        contributors, projects = list(contributors), list(projects)
        self.contributors = {row.id: row for row in contributors}
        self.projects = {row.id: row for row in projects}
        if len(self.contributors) != len(contributors) or len(self.projects) != len(projects):
            raise ValueError("Duplicate directory ID")
        self._state = State(loads={row.id: 0 for row in contributors},
                            usage={row.id: 0 for row in projects})

    def snapshot(self):
        return self._state.copy()

    def assignment(self, task_id):
        return self._state.assignments.get(task_id)

    def _insert(self, allocation):
        contributor = self.contributors[allocation.contributor_id]
        project = self.projects[allocation.project_id]
        if allocation.task_id in self._state.assignments:
            raise ValueError("Task already assigned")
        if self._state.loads[contributor.id] + allocation.units > contributor.capacity:
            raise ValueError("Capacity exceeded")
        if self._state.usage[project.id] >= project.quota:
            raise ValueError("Quota exceeded")
        self._state.assignments[allocation.task_id] = allocation
        self._state.loads[contributor.id] += allocation.units
        self._state.usage[project.id] += 1

    def commit(self, plan, fail_task=None):
        before = self.snapshot()
        try:
            for allocation in plan.allocations:
                if allocation.task_id == fail_task:
                    raise CommitFailure("Storage publication interrupted")
                self._insert(allocation)
        except Exception:
            self._state.assignments = before.assignments
            raise
        return self.snapshot()

    def release(self, task_id):
        allocation = self._state.assignments.pop(task_id, None)
        if allocation is None:
            return False
        self._state.loads[allocation.contributor_id] -= allocation.units
        self._state.usage[allocation.project_id] -= 1
        return True

    def export(self):
        state = self.snapshot()
        return dict(assignments=[row.as_dict() for row in state.assignments.values()],
                    loads=state.loads, usage=state.usage)
