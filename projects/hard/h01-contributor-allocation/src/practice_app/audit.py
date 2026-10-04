"""Independent accounting checks and operational summaries."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Audit:
    assigned_tasks: int
    assigned_units: int
    contributor_rows: tuple
    project_rows: tuple
    problems: tuple

    @property
    def consistent(self):
        return not self.problems

    def as_dict(self):
        return dict(assigned_tasks=self.assigned_tasks, assigned_units=self.assigned_units,
                    contributors=list(self.contributor_rows), projects=list(self.project_rows),
                    problems=list(self.problems), consistent=self.consistent)


def inspect(repository):
    state = repository.snapshot()
    expected_loads = {id: 0 for id in repository.contributors}
    expected_usage = {id: 0 for id in repository.projects}
    for row in state.assignments.values():
        expected_loads[row.contributor_id] += row.units
        expected_usage[row.project_id] += 1
    problems = []
    if state.loads != expected_loads:
        problems.append("load totals differ")
    if state.usage != expected_usage:
        problems.append("project totals differ")
    contributors = []
    for id, contributor in sorted(repository.contributors.items()):
        load = state.loads[id]
        if load < 0 or load > contributor.capacity:
            problems.append("capacity outside bounds: " + id)
        contributors.append(dict(id=id, load=load, remaining=contributor.capacity-load))
    projects = []
    for id, project in sorted(repository.projects.items()):
        usage = state.usage[id]
        if usage < 0 or usage > project.quota:
            problems.append("quota outside bounds: " + id)
        projects.append(dict(id=id, usage=usage, remaining=project.quota-usage))
    return Audit(len(state.assignments), sum(row.units for row in state.assignments.values()),
                 tuple(contributors), tuple(projects), tuple(problems))
