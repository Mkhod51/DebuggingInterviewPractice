"""Dispatch API and operational queue summaries."""
from dataclasses import dataclass
from .models import load_tasks, validate_limit
from .queue import Queue, ready


@dataclass(frozen=True)
class Dispatch:
    tasks: tuple
    remaining: int

    def as_dict(self):
        return dict(tasks=[row.as_dict() for row in self.tasks], remaining=self.remaining)


class QueueService:
    def __init__(self, queue):
        self.queue = queue

    def peek(self, now, limit):
        validate_limit(limit)
        return tuple(ready(self.queue.ordered(), now)[:limit])

    def dispatch(self, now, limit):
        validate_limit(limit)
        selected = ready(self.queue.ordered()[:limit], now)
        for task in selected:
            self.queue.remove(task.id)
        return Dispatch(tuple(selected), len(self.queue))

    def summary(self, now):
        tasks = self.queue.snapshot()
        available = ready(tasks, now)
        return dict(total=len(tasks), ready=len(available),
                    disabled=sum(not task.enabled for task in tasks),
                    waiting=sum(task.enabled and task.available_at > now for task in tasks))

    def enqueue(self, task):
        self.queue.enqueue(task)

    def cancel(self, task_id):
        return self.queue.remove(task_id) is not None


def service_from_file(path):
    return QueueService(Queue(load_tasks(path)))
