# M01: Contributor assignment

A local assignment service routes annotation tasks to qualified contributors and tracks their remaining capacity.

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
