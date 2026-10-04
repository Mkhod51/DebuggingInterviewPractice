"""Repository owns mutable jobs and publishes independent snapshots."""
from copy import deepcopy


class Repository:
    def __init__(self, jobs=()):
        self._jobs = {}
        for job in jobs:
            self.enqueue(job)

    def enqueue(self, job):
        if job.id in self._jobs:
            raise ValueError("Duplicate job ID")
        self._jobs[job.id] = job.copy()

    def get(self, identifier):
        return self._jobs[identifier].copy()

    def all(self):
        return [job.copy() for job in sorted(self._jobs.values(), key=lambda row: row.id)]

    def ready_ids(self, now):
        rows = [job for job in self._jobs.values()
                if job.status in {"queued", "retry_wait"} and job.due_at <= now]
        return [job.id for job in sorted(rows, key=lambda row: (row.due_at, row.id))]

    def claim(self, identifier, now):
        job = self._jobs[identifier]
        if identifier not in self.ready_ids(now):
            raise ValueError("Job is not ready")
        job.status = "running"
        job.attempts += 1
        return job.copy()

    def succeed(self, identifier, result):
        job = self._jobs[identifier]
        if job.status != "running":
            raise ValueError("Job is not running")
        job.status = "succeeded"
        job.result = deepcopy(result)
        job.error = None

    def fail(self, identifier, error, due_at=None):
        job = self._jobs[identifier]
        if job.status != "running":
            raise ValueError("Job is not running")
        job.error = str(error)
        job.result = None
        job.status = "failed" if due_at is None else "retry_wait"
        if due_at is not None:
            job.due_at = due_at

    def summary(self):
        states = {name: 0 for name in ["queued", "running", "retry_wait", "succeeded", "failed"]}
        for job in self._jobs.values():
            states[job.status] += 1
        return states
