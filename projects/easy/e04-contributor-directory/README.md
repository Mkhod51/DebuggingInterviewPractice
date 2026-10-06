# E04: Contributor directory

## Scenario

A labeling platform maintains a directory of contributors: the people who do its
annotation work. An operations tool needs to look up a person by their system ID
or email address and display a profile. It also lets operators search for active
contributors by name.

This exercise implements the backend of that directory. It builds lookup indexes
from contributor records and returns profile dictionaries that a caller could
display. There is no login flow, email delivery or web interface.

## What the terms mean

- **Contributor ID:** an exact reference issued by another system. It is an
  opaque string, meaning the directory should not infer meaning from its spelling.
- **Email normalization:** the lookup rule that ignores outer whitespace and
  letter case in email addresses. ID lookup has a different rule: exact matching.
- **Quality:** an optional score from 0 to 1 recorded on the contributor. This
  directory displays it; it does not calculate it from reviews.
- **Unknown quality:** `None`, meaning no score has been recorded. A configured
  default supplies a display value without turning the unknown score into a known one.
- **Capacity and active status:** stored profile information about available work
  capacity and whether a contributor is currently active. This exercise does not
  assign tasks or consume capacity.
- **Independent profile:** a returned dictionary the caller can edit without
  changing the underlying directory entry.

## Example of correct behavior

Suppose contributor `C01` is Alex, with email `alex@example.test` and quality
`0.8`. Contributor `C02` is Sam, whose quality is unknown. With a display default
of `0.5`, Alex's profile has `display_quality=0.8` and `quality_known=True`;
Sam's has `display_quality=0.5`, `quality=None` and `quality_known=False`.

Looking up `" ALEX@EXAMPLE.TEST "` finds Alex. Looking up the unknown ID `C99`
returns `None`. Editing the name in a returned profile must not rename the stored
contributor. These examples describe the required behavior of the directory.

## Behavior contract

- Contributor IDs are opaque, case-sensitive strings; `A` and `a` are distinct.
- Email search strips outer whitespace and ignores case. Duplicate normalized emails are errors.
- Quality is optional: None means unknown and uses the supplied display default; zero is a real quality value.
- Quality values and display defaults lie in `[0, 1]`; capacity is nonnegative.
- Missing lookups return None. Search returns active profiles only, sorted by exact ID.
- Returned profile dictionaries are independent. Directory creation rejects duplicate exact IDs.

## Incident

Profiles with similar capitalization disappear or collide, and contributors with a recorded zero quality score receive the unknown-score display value.

## Start here

### Codebase map

All application modules are under `src/practice_app/`:

| File | Responsibility |
| --- | --- |
| `models.py` | Contributor fields, validation, email normalization and file loading. |
| `directory.py` | ID/email indexes, duplicate checks and active-contributor search. |
| `service.py` | Display values, profile rendering and public lookup methods. |
| `tests/test_directory.py` | Lookup and display behavior, including optional scores. |
| `fixtures/directory.json` | Contributor profiles for an end-to-end local lookup. |

The public entry point is `practice_app.service.DirectoryService.profile`. Explore the modules and local fixtures
as needed. No network is used by this application or its tests. Tested on Python
3.14.0; metadata allows Python 3.11+, which has not been separately verified.
Practice session target: 20–30 minutes (our design choice).

From this project directory, including a standalone copy:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
python -m pytest -q
python -m pytest -q tests/test_directory.py::test_identifiers_are_case_sensitive
```

Installation may download pytest and build tools. Starting application test failures
are intentional. Installation, imports and test discovery must work.

Diagnose and correct application behavior, add regression tests and explain your
evidence and findings. You may add tests. Existing tests and expected outputs are
the contract: do not delete, skip, xfail or weaken them to obtain a pass. A passing
suite is evidence, not proof of correctness for every possible input.
