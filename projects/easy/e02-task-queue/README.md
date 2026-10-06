# E02: Task queue

## Scenario

Imagine a labeling platform with a backlog of jobs waiting to be processed. A job
might contain a batch of text that needs labels. Some jobs are urgent, some have
been paused, and some are scheduled for later. A worker asks the platform for more
work whenever it has space to take it.

Your application manages the backlog and chooses which jobs to hand over. If a
worker has two free slots, it can receive at most two jobs on that request. Each
job uses one slot, regardless of its payload. This exercise stops at handing over
the jobs: it does not run the labeling work, start worker processes or track job
completion.

## What the terms mean

- **Task/job:** one item of work. It has a unique `id` and a `payload` describing
  the work; the queue does not interpret that payload.
- **Queue:** the collection of jobs still waiting to be handed over. Selection
  follows priority rules rather than simply taking the oldest inserted job.
- **Worker slot / `limit`:** how many jobs the worker can accept on this dispatch
  request. A limit of zero means it cannot accept any right now.
- **Priority:** an integer urgency level; a larger number means more urgent.
- **`created_at`:** when a job entered the system, used to break priority ties.
- **`available_at`:** the earliest time a job may be handed over. A job can exist
  in the queue before it is available.
- **Ready:** enabled and available at the supplied time `now`. Disabled jobs are
  paused; scheduled jobs wait until their availability time.
- **Dispatch versus peek:** dispatch hands jobs over and removes them from the
  queue. Peek shows what would be selected without removing anything.

## Example of correct behavior

At `now=100`, a worker asks for `limit=2`. All these jobs were created at time 0:

| ID | Priority | Available at | Enabled | Meaning at time 100 |
| --- | --- | --- | --- | --- |
| urgent | 9 | 80 | yes | Ready |
| ordinary | 2 | 90 | yes | Ready |
| later | 12 | 120 | yes | Scheduled for the future |
| paused | 10 | 80 | no | Paused |

The worker should receive `urgent`, then `ordinary`. Both are removed, so the
dispatch result has two tasks and `remaining=2`. The other jobs stay queued even
though their priorities are higher. `remaining` counts all queued jobs, including
ones that are not ready. Peeking at the original backlog with these inputs would
return the same two jobs while leaving all four queued. This is the behavior to compare
with the starter application.

## Behavior contract

- Higher integer priority is dispatched first; ties use earlier creation time, then task ID.
- A task is ready when enabled and `available_at <= now`. Disabled and future tasks remain queued.
- Dispatch at most `limit` ready tasks; limit may be zero but never negative.
- Dispatch removes exactly the returned tasks. Peek is read-only and uses the same ordering.
- IDs are unique. Removing unknown IDs is harmless; enqueueing duplicate IDs is an error.
- All clock values are explicit integer seconds; execution does not sleep.

## Incident

Workers sometimes receive low-priority tasks ahead of urgent work, and dispatch leaves empty slots despite ready jobs remaining.

## Start here

### Codebase map

All application modules are under `src/practice_app/`:

| File | Responsibility |
| --- | --- |
| `models.py` | Task fields, readiness rules and fixture loading. |
| `queue.py` | Queue storage, ordering, enqueueing and removal. |
| `service.py` | Dispatch, peek, cancellation and queue summaries. |
| `tests/test_queue.py` | Examples of ordering, readiness and queue changes. |
| `fixtures/queue.json` | A local backlog you can load through `service_from_file`. |

The public entry point is `practice_app.service.QueueService.dispatch`. Explore the modules and local fixtures
as needed. No network is used by this application or its tests. Tested on Python
3.14.0; metadata allows Python 3.11+, which has not been separately verified.
Practice session target: 20–30 minutes (our design choice).

From this project directory, including a standalone copy:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
python -m pytest -q
python -m pytest -q tests/test_queue.py::test_urgent_jobs_are_selected_first
```

Installation may download pytest and build tools. Starting application test failures
are intentional. Installation, imports and test discovery must work.

Diagnose and correct application behavior, add regression tests and explain your
evidence and findings. You may add tests. Existing tests and expected outputs are
the contract: do not delete, skip, xfail or weaken them to obtain a pass. A passing
suite is evidence, not proof of correctness for every possible input.
