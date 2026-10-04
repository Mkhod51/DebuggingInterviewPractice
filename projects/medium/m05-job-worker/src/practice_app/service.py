"""Local worker assembly and state export."""
import json
from pathlib import Path
from .models import Job, Clock, RetryPolicy
from .repository import Repository
from .handler import FakeHandler
from .worker import Worker


def worker_from_file(path):
    data = json.loads(Path(path).read_text())
    jobs = [Job(**row) for row in data["jobs"]]
    clock = Clock(data.get("now", 0))
    policy = RetryPolicy(**data.get("policy", {}))
    return Worker(Repository(jobs), FakeHandler(data["scripts"]), clock, policy)


def export_jobs(worker):
    return json.dumps([job.as_dict() for job in worker.repository.all()], sort_keys=True)
