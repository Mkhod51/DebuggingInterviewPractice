# Self-contained context for a new debugging practice chat

## Purpose and evidence

I am preparing for Scale AI's Software Engineering Intern (Summer 2027), London,
debugging practical. I chose Python throughout. My supplied interview description
says HackerRank hosts it, Python and TypeScript are available, and candidates must
navigate an unfamiliar codebase, debug failing test cases and explain incorrect
behavior and corrections. This direct information is stronger than public reports.
My own time limit, project length, defect count and official grading are not confirmed.
Public reports from other candidates/roles motivate modular debugging practice;
our 15 original exercises, sizes, session targets and rubric are design choices.
No internal Scale knowledge or ML expertise is needed. Research date: October 4,
2026. Exponent's supplied account could not be fetched; do not treat its summary
as independently verified. Source links and access details are in interview-research.md.

Repository:
`/Users/mkhoder/Career/Internship apps /IndividualApps/ScaleAI/InterviewPrep/DebugPractice/DebugPracice`

All fifteen exercises and reference packages are implemented and individually
verified. Final whole-collection fresh-copy verification is in progress. Read the
actual BUILD_STATUS.md for updates. No learner practice accomplishments are known.

## Catalog and structure

| ID | Project | Path under projects/ |
| --- | --- | --- |
| E01 | [Annotation reports](../projects/easy/e01-annotation-reports/README.md) | `easy/e01-annotation-reports` |
| E02 | [Task queue](../projects/easy/e02-task-queue/README.md) | `easy/e02-task-queue` |
| E03 | [Dataset importer](../projects/easy/e03-dataset-importer/README.md) | `easy/e03-dataset-importer` |
| E04 | [Contributor directory](../projects/easy/e04-contributor-directory/README.md) | `easy/e04-contributor-directory` |
| E05 | [Quality scores](../projects/easy/e05-quality-scores/README.md) | `easy/e05-quality-scores` |
| M01 | [Contributor assignment](../projects/medium/m01-contributor-assignment/README.md) | `medium/m01-contributor-assignment` |
| M02 | [Paginated dataset client](../projects/medium/m02-paginated-client/README.md) | `medium/m02-paginated-client` |
| M03 | [Evaluation runner](../projects/medium/m03-evaluation-runner/README.md) | `medium/m03-evaluation-runner` |
| M04 | [Prediction cache](../projects/medium/m04-prediction-cache/README.md) | `medium/m04-prediction-cache` |
| M05 | [Retrying job worker](../projects/medium/m05-job-worker/README.md) | `medium/m05-job-worker` |
| H01 | [Contributor allocation](../projects/hard/h01-contributor-allocation/README.md) | `hard/h01-contributor-allocation` |
| H02 | [Incremental sync](../projects/hard/h02-incremental-sync/README.md) | `hard/h02-incremental-sync` |
| H03 | [Asynchronous evaluation](../projects/hard/h03-async-evaluation/README.md) | `hard/h03-async-evaluation` |
| H04 | [Model gateway](../projects/hard/h04-model-gateway/README.md) | `hard/h04-model-gateway` |
| H05 | [Annotation workflow](../projects/hard/h05-annotation-workflow/README.md) | `hard/h05-annotation-workflow` |

Each project contains README.md, pyproject.toml, src/practice_app/, tests/ and
fixtures/. Projects are standalone: no root test configuration or shared application
imports. Each uses its own environment. Easy targets: 20–30 minutes, 120–220 application
lines, 2–3 modules, 1–2 defects. Medium: 35–45 minutes, 220–400 lines, 3–5 modules,
2–3 defects. Hard: 60 minutes, 350–650 lines, 4–7 modules, 3–5 defects. Sizes are
guidelines; implementations are intentionally compact, with difficulty from causal
distance, interactions and state. The number and difficulty split are exact (5 each).

`codex/debugging-practice` is the practice branch and primary workspace. `solutions`
is local and contains `solutions/<difficulty>/<project>/` packages with staged hints,
explanations, reference.patch, extra_tests and verification.json. Its projects remain
the original buggy source. Never merge solutions into practice. Instructor materials
must remain off the practice branch, working tree and history. Attempts live under
Gitignored attempts/. The initial build authorized local branches/commits and instructor
verification; it did not authorize push, PR, publication or messaging others.

## Tested setup and attempt workflow

Python 3.14.0, pytest 9.0.2; setuptools==82.0.1 is the isolated build requirement.
Metadata permits Python 3.11+, but other versions are unverified. No runtime third-party
packages, keys, network calls, Docker, servers, GPU or ML services are needed.
Installation may download development/build packages.

From the repository root:

```sh
python3 scripts/start_attempt.py E01 --name first
cd attempts/e01-first
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
python -m pytest -q
python -m pytest -q tests/test_reports.py::test_empty_report_is_exportable
```

The helper accepts case-insensitive E01–E05, M01–M05 and H01–H05. Use a new name
for a new attempt; it refuses collisions. Without --name it uses a UTC timestamp.
Invoking the helper with an absolute path works from any caller directory. Each
README lists its own exact selected-test command. Keep projects in separate environments
because every package is named practice_app. A manual standalone copy works too.

Starting suites intentionally have both passing and failing application tests. Do
not weaken, skip, xfail or remove existing assertions. You may add regression tests.
Installation/import/discovery failures are infrastructure problems, not planted puzzles.
Passing tests alone do not establish correctness for every possible input.

## Default coach mode

If missing, ask for my current project ID, attempt path, failing output and observations.
Use README behavior rules and my evidence to help form competing hypotheses. Ask
what a prediction would look like at a boundary and help design a small experiment.
Keep observed values, hypotheses and untested guesses distinct. Help me trace input,
state and output across modules and prepare a spoken explanation.

Do not silently fix my attempt, inspect solution contents or reveal root causes.
Reveal one staged hint only when I request it. Do not read later hints or explanations
in anticipation. I may explicitly request full solutions, direct fixes, a review or
further exercise development; that request overrides default coaching. Review a fix
against the contract, unchanged visible tests, sensible regression coverage and an
explanation supported by evidence. Our rubric covers diagnosis, evidence, correctness,
coverage, communication and use of time; it is not Scale's official grading.

When tools are available, inspect actual repo/attempt state and applicable AGENTS.md
before work. Preserve changes and previous attempts. Without tools, request relevant
snippets/output. Never imply a new chat already has filesystem access, remembers my
progress or knows which tests I ran.

## Deliberate hint and solution access

WARNING: these commands can reveal answers. Run only the level I requested.
From the repo, reveal E01 direction only:

```sh
git show solutions:solutions/easy/e01-annotation-reports/hints/01-direction.md
```

The next files are 02-investigation.md and 03-root-cause.md, each only on request.
Package instructions, including safe evaluation of an attempt and applying an
application-only patch to a fresh copy:

```sh
git show solutions:solutions/README.md
```

To obtain just one package without switching branches:

```sh
package_dir=$(mktemp -d)
git archive solutions solutions/easy/e01-annotation-reports | tar -x -C "$package_dir"
package="$package_dir/solutions/easy/e01-annotation-reports"
```

From an attempt with its own environment, extra tests run without replacing source:

```sh
.venv/bin/python -m pytest -q tests "$package/extra_tests"
```

Request full solutions before examining explanation.md, reference.patch or
verification.json. A patch is an example, not the only valid implementation. Never
apply it to my active attempt unless I explicitly request a direct fix. Use a fresh
original copy at the revision recorded in the solution package for reference checks.

## Practice method and remaining builder work

Reproduce → read the contract → trace → hypothesize → instrument → correct → add
regression coverage → rerun → explain symptom, expected behavior, evidence, cause,
correction and verification. Start untimed; use a 60-minute hard mock as our target,
not a confirmed duration for my interview. Helper checks run with
`python3 -m unittest discover -s scripts -v`. Do not count test runs as learner sessions.

Remaining implementation work: finish solution workflow documentation, run the final
fresh-copy collection audit and record current branch/commit verification. There are
no known unresolved application infrastructure issues in completed checkpoints.

## Editable learner state (not yet supplied)

- Current exercise: unknown
- Attempt directory: unknown
- Completed exercises: unknown/not supplied
- Elapsed time: unknown
- Hints used: unknown
- Hypotheses and observations: not supplied
- Next learner step: choose a project and create an attempt
