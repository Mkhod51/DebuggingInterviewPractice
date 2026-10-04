"""Portable local orchestration with explicitly controlled completion order."""
import asyncio
from .models import load_input
from .controlled_model import ControlledModel
from .runner import AsyncRunner


async def run_controlled(cases, outcomes, release_order):
    cases = list(cases)
    ids = [case.id for case in cases]
    if sorted(release_order) != sorted(ids):
        raise ValueError("Release order must contain every input ID exactly once")
    model = ControlledModel(outcomes)
    runner = AsyncRunner(model, max_concurrency=max(1, len(cases)))
    task = asyncio.create_task(runner.run(cases))
    try:
        for _ in cases:
            await model.next_started()
        for identifier in release_order:
            model.release(identifier)
            await model.next_finished()
        return await task
    finally:
        if not task.done():
            task.cancel()
            model.release_all()
            await asyncio.gather(task, return_exceptions=True)


def evaluate_file(path):
    cases, outcomes, order = load_input(path)
    return asyncio.run(run_controlled(cases, outcomes, order))
