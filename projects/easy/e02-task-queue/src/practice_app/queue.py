"""Local queue storage and deterministic ordering."""


class Queue:
    def __init__(self, tasks=()):
        self._tasks = {}
        for task in tasks:
            self.enqueue(task)

    def enqueue(self, task):
        if task.id in self._tasks:
            raise ValueError("Duplicate task ID")
        self._tasks[task.id] = task

    def remove(self, task_id):
        return self._tasks.pop(task_id, None)

    def get(self, task_id):
        return self._tasks.get(task_id)

    def ordered(self):
        return sorted(self._tasks.values(), key=lambda task: (-task.priority, task.created_at, task.id))

    def snapshot(self):
        return list(self._tasks.values())

    def __len__(self):
        return len(self._tasks)

    def export(self):
        return [task.as_dict() for task in self.ordered()]


def ready(tasks, now):
    return [task for task in tasks if task.ready(now)]
