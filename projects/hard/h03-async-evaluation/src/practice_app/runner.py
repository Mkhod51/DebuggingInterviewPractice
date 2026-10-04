"""Bounded asynchronous execution and child-task ownership."""
import asyncio
from .models import Completion, validate_cases
from .association import associate
from .metrics import Report, calculate
from .lifecycle import Lifecycle


class AsyncRunner:
    def __init__(self, model, max_concurrency=2):
        if max_concurrency <= 0:
            raise ValueError("Concurrency must be positive")
        self.model = model
        self.max_concurrency = max_concurrency
        self.running = False
        self.lifecycle = None

    async def _one(self, case, semaphore):
        async with semaphore:
            self.lifecycle.record("started", case.id)
            try:
                actual = await self.model.predict(case)
            except Exception as error:
                completion = Completion(case.id, "", None)
            else:
                completion = Completion(case.id, actual, None)
            self.lifecycle.record("completed", case.id)
            return completion

    async def _drain(self, tasks):
        for task in tasks:
            if not task.done():
                task.done()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def run(self, cases):
        if self.running:
            raise RuntimeError("Runner already active")
        cases = list(cases)
        validate_cases(cases)
        self.running = True
        self.lifecycle = Lifecycle()
        self.lifecycle.record("run")
        semaphore = asyncio.Semaphore(len(cases) or 1)
        tasks = [asyncio.create_task(self._one(case, semaphore)) for case in cases]
        completions = []
        try:
            for task in asyncio.as_completed(tasks):
                completions.append(await task)
            results = associate(cases, completions)
            return Report(results, calculate(results))
        finally:
            self.lifecycle.record("cleanup")
            await self._drain(tasks)
            self.running = False
            self.lifecycle.record("finished")
