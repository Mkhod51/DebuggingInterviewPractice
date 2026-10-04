# H01: Contributor allocation

A batch allocation pipeline reserves contributor capacity and project quotas, publishes a complete plan atomically, and supports repeated runs.

## Behavior contract

- A contributor must be active, authorized for the project, speak its language and hold every certification.
- Each task has positive units and integer priority. Process highest priority first, then task ID.
- Select the eligible contributor with lowest planned unit load, then contributor ID.
- Contributor capacity is measured in units; project quota counts assignments. Exact limits are allowed.
- Plans account for existing assignments and every reservation made earlier in the same plan.
- Preview is read-only. A successful run commits the plan atomically. An injected commit failure
  must leave assignments, loads and project usage exactly as before the run.
- Already assigned task IDs are ignored on repeated runs. Task IDs represent stable task data.
- Unknown project IDs and duplicate task IDs are errors. Unallocated tasks remain available for later runs.
- Returned snapshots are independent copies; audit totals must agree with stored assignments.

## Incident

Operators see empty allocations for authorized contributors. After adjusting inputs, large batches and retries sometimes disagree with capacity and audit totals.

## Start here

The public entry point is `practice_app.service.AllocationService.run`. Explore the modules and local fixtures
as needed. No network is used by this application or its tests. Tested on Python
3.14.0; metadata allows Python 3.11+, which has not been separately verified.
Practice session target: 60 minutes (our design choice).

From this project directory, including a standalone copy:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
python -m pytest -q
python -m pytest -q tests/test_allocation.py::test_project_authorization_uses_project_membership
```

Installation may download pytest and build tools. Starting application test failures
are intentional. Installation, imports and test discovery must work.

Diagnose and correct application behavior, add regression tests and explain your
evidence and findings. You may add tests. Existing tests and expected outputs are
the contract: do not delete, skip, xfail or weaken them to obtain a pass. A passing
suite is evidence, not proof of correctness for every possible input.
