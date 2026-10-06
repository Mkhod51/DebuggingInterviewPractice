# M01: Contributor assignment

## Scenario

A labeling team has a batch of tasks to distribute among human contributors.
Each task requires particular skills and a language, and contributors have
different qualifications and finite capacity. The operations team wants the
service to choose a suitable person for each task and keep its workload records
accurate as assignments are made and released.

This application accepts tasks in a specified order, returns their assignments
and any unassigned task IDs, and remembers assignments across calls. It chooses
who should do the work; it does not execute the annotation work or decide whether
the eventual labels are correct.

## What the terms mean

- **Contributor:** a person with a set of skills, supported languages, capacity
  and an active flag. Only active contributors can receive new work.
- **Task requirements:** the language and every skill needed for that task.
  A contributor must meet the whole set of requirements.
- **Units:** the task's workload cost. A three-unit task consumes three units of
  contributor capacity even though it creates only one assignment.
- **Load and remaining capacity:** units already assigned to a contributor,
  and the capacity left after accounting for those assignments.
- **Assignment:** a stored link between a task ID and a contributor ID, including
  the units reserved for that task.
- **Idempotent assignment:** asking to assign an already assigned task again
  returns its existing assignment without allocating the work a second time.
- **Release:** removing an assignment and freeing the units it reserved.

## Example of correct behavior

Alex is active, speaks English, has the required `text` skill and has capacity 5.
Alex already has one unit of assigned work. A new English text task costing two
units can be assigned to Alex: the load becomes 3 and the remaining capacity is 2.
Another task costing three units cannot fit unless capacity is freed or another
qualified contributor is available.

Submitting the first task again should keep its original assignment and load.
Releasing it should remove that assignment and bring Alex's load back to 1.
When several people qualify, the service chooses the one with the lowest current
unit load, using contributor ID to break ties. These describe required behavior;
the starter application contains failures to investigate.

## Behavior contract

- Contributors must be active, speak the task language and possess every required skill.
- A task consumes its positive `units`; total assigned units may equal capacity but cannot exceed it.
- Among eligible contributors choose the smallest current load, then lexicographic contributor ID.
- Process tasks in input order. Assigned task IDs are idempotent; unassigned tasks may be retried later.
- Releasing an assignment frees exactly its units. Returned assignment lists are independent copies.
- Unknown contributor IDs, duplicate directory IDs and invalid capacities/units are errors.
- Tasks have unique IDs within one request; an existing ID represents the same task across calls.

## Incident

The service leaves some exactly fitting tasks unassigned, accepts partially qualified contributors and understates load after larger assignments.

## Start here

### Codebase map

All application modules are under `src/practice_app/`:

| File | Responsibility |
| --- | --- |
| `models.py` | Contributor, task and assignment records; fixture loading. |
| `rules.py` | Eligibility decisions and candidate ranking. |
| `repository.py` | Stored assignments, contributor loads and remaining capacity. |
| `service.py` | Batch assignment, repeat requests and release operations. |
| `tests/test_assignment.py` | Qualification, accounting and repeated-call examples. |
| `fixtures/batch.json` | A local contributor directory and batch of tasks. |

The public entry point is `practice_app.service.AssignmentService.assign`. Explore the modules and local fixtures
as needed. No network is used by this application or its tests. Tested on Python
3.14.0; metadata allows Python 3.11+, which has not been separately verified.
Practice session target: 35–45 minutes (our design choice).

From this project directory, including a standalone copy:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
python -m pytest -q
python -m pytest -q tests/test_assignment.py::test_all_required_skills_are_necessary
```

Installation may download pytest and build tools. Starting application test failures
are intentional. Installation, imports and test discovery must work.

Diagnose and correct application behavior, add regression tests and explain your
evidence and findings. You may add tests. Existing tests and expected outputs are
the contract: do not delete, skip, xfail or weaken them to obtain a pass. A passing
suite is evidence, not proof of correctness for every possible input.
