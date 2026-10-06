# H01: Contributor allocation

## Scenario

An annotation operation has tasks from several projects to distribute among human
contributors. Contributors may work only on authorized projects and must have
the task's language and certifications. The operation also limits both how much
work each person can carry and how many assignments each project can receive.

Instead of saving assignments one at a time as it chooses them, this application
first builds a batch plan. Operators can preview that plan, then commit it to
local storage and inspect an audit report. A failed commit must not leave half
the plan saved. Repeated runs must also recognize work that was already allocated.
The exercise models allocation and accounting, rather than execution of the tasks.

## What the terms mean

- **Task:** a work item belonging to one project, with required certifications,
  language, workload `units` and urgency `priority`.
- **Project authorization:** explicit membership in a contributor's allowed
  projects. A contributor's qualifications alone do not grant project access.
- **Capacity / load:** the maximum and currently allocated work units for a
  contributor. Tasks may cost different numbers of units.
- **Project quota / usage:** the maximum and currently allocated number of
  assignments for a project. These count tasks, rather than their work units.
- **Plan / reservation:** proposed assignments and the capacity/quota they would
  consume. Later decisions in the same plan must account for earlier reservations.
- **Preview:** building the proposed plan without saving it.
- **Atomic commit:** saving all of a plan's assignments and accounting changes,
  or none of them if the commit fails.
- **Audit:** checking whether stored assignments agree with contributor loads
  and project usage. A snapshot is an independent copy of that stored state.

## Example of correct behavior

One eligible contributor has capacity 5 and no existing assignments. Project `p`
has quota 2. Its tasks, in priority order, cost 3, 2 and 1 units. The proposed plan
should allocate the first two tasks, using all 5 contributor units and both
project assignments. The third task remains unallocated for a later run.

A preview leaves the stored load and usage at zero. A successful run saves two
assignments, load 5 and project usage 2; the audit agrees with those totals.
If saving the second assignment fails, none of that new plan remains stored.
Running the same tasks after a successful commit creates no duplicate assignments.
These are the intended results to compare with the starter application.

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

### Codebase map

All application modules are under `src/practice_app/`:

| File | Responsibility |
| --- | --- |
| `models.py` | Contributors, projects, tasks, allocations and accounting state. |
| `eligibility.py` | Project access, qualification checks and candidate ranking. |
| `planner.py` | Batch validation and proposed allocations on a copied state. |
| `repository.py` | Stored assignments, plan commits, release and snapshots. |
| `audit.py` | Checks comparing assignments with loads and project usage. |
| `service.py` | Preview/run coordination and audit results. |
| `tests/test_allocation.py` | Constraints, failed commits and repeated-run examples. |
| `fixtures/batch.json` | Local contributors, projects and tasks for a complete run. |

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
