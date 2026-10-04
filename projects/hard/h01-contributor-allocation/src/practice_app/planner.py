"""Build a deterministic allocation plan on an isolated snapshot."""
from dataclasses import dataclass
from .eligibility import rank
from .models import Allocation


@dataclass(frozen=True)
class Plan:
    allocations: tuple
    unallocated: tuple

    @property
    def total_units(self):
        return sum(row.units for row in self.allocations)

    def as_dict(self):
        return dict(allocations=[row.as_dict() for row in self.allocations],
                    unallocated=list(self.unallocated), total_units=self.total_units)


def validate_tasks(tasks, projects):
    ids = [row.id for row in tasks]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate task ID")
    for task in tasks:
        if task.project not in projects:
            raise ValueError("Unknown project")


def build_plan(contributors, projects, tasks, initial):
    tasks = list(tasks)
    validate_tasks(tasks, projects)
    state = initial.copy()
    allocations = []
    unallocated = []
    for task in sorted(tasks, key=lambda row: (-row.priority, row.id)):
        project = projects[task.project]
        available = rank(contributors, task, project, state)
        if not available:
            unallocated.append(task.id)
            continue
        worker = available[0]
        allocation = Allocation(task.id, task.project, worker.id, task.units)
        allocations.append(allocation)
        state.loads[worker.id] = task.units
        state.usage[project.id] += 1
        state.assignments[task.id] = allocation
    return Plan(tuple(allocations), tuple(unallocated))
