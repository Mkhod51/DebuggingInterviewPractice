# H05: Annotation workflow

## Scenario

A labeling platform tracks each item from waiting for work to final review. A
contributor claims an item, submits a label, and a different person reviews it.
Rejected work may be returned to the queue for another attempt. Several callers
can hold an older view of an item, so the platform must prevent outdated requests
from overwriting newer work.

This application implements those commands and records an event for every
successful transition. It keeps the current task state and event history
consistent even if event publication fails. Storage, publisher and clock are
local exercise components; there is no UI, message broker or external database.

## What the terms mean

- **Work item:** a task with an ID, current state, version, owner, submission
  data and review data.
- **Claim / owner:** reserving queued work for a contributor. Only that owner
  can submit it; another person must review it.
- **Submission:** a nonempty JSON object containing the contributor's work,
  such as `{"label": "yes"}`.
- **Review:** approval with a numeric score, or rejection with a reason.
  The approval decision is supplied explicitly; it is not inferred from the score.
- **Requeue:** making rejected work available for a fresh claim and submission,
  clearing the previous attempt's owner, work and review.
- **Version / `expected_version`:** a counter of successful transitions and the
  version the caller believes it is changing. A mismatch means the request is stale.
- **Event ledger:** the local history of successful transitions, including task
  ID, actor, action, resulting state, new version and timestamp.
- **Publication:** handing an event to the fake publisher. A publication failure
  must leave neither a changed task nor a new local event behind.
- **Audit:** checking that each task agrees with its latest local event.

## Example of correct behavior

Task `t1` starts queued at version 0:

| Command | Actor | Expected version | Resulting state | New version |
| --- | --- | --- | --- | --- |
| claim | alex | 0 | claimed | 1 |
| submit `{"label": "yes"}` | alex | 1 | submitted | 2 |
| approve with score 0.8 | sam | 2 | approved | 3 |

Afterward, the ledger should have three events whose versions and resulting
states match those transitions. If Sam rejects instead, the state becomes
rejected and the work can be requeued for another attempt. If a caller tries a
command with an old expected version, it fails without changing task or ledger.
If publication fails during the initial claim, the item remains queued at
version 0 and the same claim can safely be retried. These describe required
behavior to compare with the starter engine.

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

### Codebase map

All application modules are under `src/practice_app/`:

| File | Responsibility |
| --- | --- |
| `models.py` | Work items, transition events, submission validation and clock. |
| `policy.py` | Actor, owner, state, review and expected-version checks. |
| `transitions.py` | Claim, submit, review and requeue state transformations. |
| `store.py` | Stored task state, event ledger and commit behavior. |
| `publisher.py` | Local publication and a controlled failure before publishing. |
| `engine.py` | Public commands, event construction and fixture loading. |
| `audit.py` | State/event consistency checks and task timelines. |
| `tests/test_workflow.py` | Full lifecycles, stale commands and publication failures. |
| `fixtures/workflow.json` | Persisted work items and a sequence of local commands. |

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
