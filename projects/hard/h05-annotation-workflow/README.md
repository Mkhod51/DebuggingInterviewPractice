# H05: Annotation workflow

An annotation workflow engine coordinates claims, submissions and reviews while keeping task state, versioned events and publication consistent.

## Behavior contract

- States: queued → claimed → submitted → approved or rejected; only rejected work may be requeued.
- Each transition checks the caller’s expected_version and increments version exactly once. Stale requests fail without changes.
- Claims require a queued task and a nonempty actor; only the owner may submit. Submission data is a nonempty JSON object.
- Review requires submitted work and a reviewer different from the owner. Approval requires finite score in `[0,1]`;
  rejection requires a nonempty reason and records no score. Zero is a valid approval score.
- Requeue clears owner, submission and review. New claims and submissions must not inherit previous work.
- Every successful transition appends one event with matching task ID, new version, actor and resulting state.
- Publication failure restores task and local event ledger completely. The fake publisher fails before publishing;
  retrying with the same expected_version must be safe.
- Snapshots, events and submission data are independent copies. Audit compares the latest event with current task state.
- Fixtures may contain persisted valid task states. All clocks and publishers are controlled and local.

## Incident

Owners cannot submit their work. Rejected items appear approved, requeues retain old data, and failed publications leave phantom events in the audit.

## Start here

The public entry point is `practice_app.engine.Workflow`. Explore the modules and local fixtures
as needed. No network is used by this application or its tests. Tested on Python
3.14.0; metadata allows Python 3.11+, which has not been separately verified.
Practice session target: 60 minutes (our design choice).

From this project directory, including a standalone copy:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
python -m pytest -q
python -m pytest -q tests/test_workflow.py::test_owner_can_submit_claimed_work
```

Installation may download pytest and build tools. Starting application test failures
are intentional. Installation, imports and test discovery must work.

Diagnose and correct application behavior, add regression tests and explain your
evidence and findings. You may add tests. Existing tests and expected outputs are
the contract: do not delete, skip, xfail or weaken them to obtain a pass. A passing
suite is evidence, not proof of correctness for every possible input.
