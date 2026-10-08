"""Local assignment storage, with capacity accounting."""
from .models import Assignment


class Repository:
    def __init__(self, contributors):
        contributors = list(contributors)
        self._contributors = {row.id: row for row in contributors}
        if len(self._contributors) != len(contributors):
            raise ValueError("Duplicate contributor ID")
        self._loads = {row.id: 0 for row in contributors}
        self._assignments = {}

    def contributors(self):
        return list(self._contributors.values())

    def contributor(self, contributor_id):
        return self._contributors[contributor_id]

    def load(self, contributor_id):
        return self._loads[contributor_id]

    def remaining(self, contributor_id):
        contributor = self.contributor(contributor_id)
        return contributor.capacity - self.load(contributor_id)

    def assignment(self, task_id):
        return self._assignments.get(task_id)

    def assignments(self):
        return list(self._assignments.values())

    def record(self, task, contributor):
        existing = self.assignment(task.id)
        if existing is not None:
            return existing
        stored = self.contributor(contributor.id)
        if stored != contributor:
            raise ValueError("Contributor differs from directory")
        if self.remaining(contributor.id) < task.units:
            raise ValueError("Capacity exceeded")
        assignment = Assignment(task.id, contributor.id, task.units)
        self._loads[contributor.id] += task.units
        self._assignments[task.id] = assignment
        return assignment

    def release(self, task_id):
        assignment = self._assignments.pop(task_id, None)
        if assignment is None:
            return False
        self._loads[assignment.contributor_id] -= assignment.units
        return True

    def summary(self):
        return [dict(id=row.id, assigned=self.load(row.id), remaining=self.remaining(row.id))
                for row in sorted(self.contributors(), key=lambda row: row.id)]

    def export(self):
        return [row.as_dict() for row in self.assignments()]
