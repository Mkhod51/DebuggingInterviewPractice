# Python debugging interview practice

Fifteen independent Python projects for preparing for Scale AI's Software Engineering
Intern (Summer 2027), London, debugging practical. Your supplied description confirms
HackerRank, Python/TypeScript, unfamiliar code and failing cases; the session durations,
project sizes and rubric below are our practice choices. No ML knowledge is required.

All fifteen projects and their local reference packages are implemented. Final
fresh-copy verification is in progress; see [build status](docs/BUILD_STATUS.md).
Starting tests intentionally fail because of application behavior. Setup, imports
and test discovery should succeed. Existing tests and README rules are the contract.

## Start an attempt

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

Use another name for another attempt. Existing attempts are never overwritten.
The helper also works when invoked by absolute path from another directory. It copies
only one standalone project and excludes environments, caches and build outputs.
You may also copy any project manually and use its README commands without this repo.

Python **3.14.0** and pytest **9.0.2** are tested. Packages declare Python 3.11+;
other Python versions have not been separately verified. Each project pins pytest
and its setuptools build backend. Application code uses only the standard library.
Dependency installation may need network access; running exercises requires none.
Use a separate environment for every exercise because they share package name
`practice_app`. Do not run all projects in one pytest session.

## Catalog

| ID | Project | Path under projects/ |
| --- | --- | --- |
| E01 | [Annotation reports](projects/easy/e01-annotation-reports/README.md) | `easy/e01-annotation-reports` |
| E02 | [Task queue](projects/easy/e02-task-queue/README.md) | `easy/e02-task-queue` |
| E03 | [Dataset importer](projects/easy/e03-dataset-importer/README.md) | `easy/e03-dataset-importer` |
| E04 | [Contributor directory](projects/easy/e04-contributor-directory/README.md) | `easy/e04-contributor-directory` |
| E05 | [Quality scores](projects/easy/e05-quality-scores/README.md) | `easy/e05-quality-scores` |
| M01 | [Contributor assignment](projects/medium/m01-contributor-assignment/README.md) | `medium/m01-contributor-assignment` |
| M02 | [Paginated dataset client](projects/medium/m02-paginated-client/README.md) | `medium/m02-paginated-client` |
| M03 | [Evaluation runner](projects/medium/m03-evaluation-runner/README.md) | `medium/m03-evaluation-runner` |
| M04 | [Prediction cache](projects/medium/m04-prediction-cache/README.md) | `medium/m04-prediction-cache` |
| M05 | [Retrying job worker](projects/medium/m05-job-worker/README.md) | `medium/m05-job-worker` |
| H01 | [Contributor allocation](projects/hard/h01-contributor-allocation/README.md) | `hard/h01-contributor-allocation` |
| H02 | [Incremental sync](projects/hard/h02-incremental-sync/README.md) | `hard/h02-incremental-sync` |
| H03 | [Asynchronous evaluation](projects/hard/h03-async-evaluation/README.md) | `hard/h03-async-evaluation` |
| H04 | [Model gateway](projects/hard/h04-model-gateway/README.md) | `hard/h04-model-gateway` |
| H05 | [Annotation workflow](projects/hard/h05-annotation-workflow/README.md) | `hard/h05-annotation-workflow` |

| Difficulty | Session target | Application size guideline | Modules | Defects guideline |
| --- | --- | --- | --- | --- |
| Easy | 20–30 min | 120–220 lines | 2–3 | 1–2 |
| Medium | 35–45 min | 220–400 lines | 3–5 | 2–3 |
| Hard | 60 min | 350–650 lines | 4–7 | 3–5 |

These are design targets, not official Scale requirements. Some implementations are
smaller than the size guidelines; they retain healthy behavior and multi-module
interactions without padding. Choose a 60-minute hard mock after untimed practice.

## Working and coaching

The primary branch is `codex/debugging-practice`; `main` retains the original commit.
The separate local `solutions` branch retains buggy projects and adds instructor
packages. Never merge it into the practice branch. No push, PR or publication was made.

[LLM_CONTEXT.md](docs/LLM_CONTEXT.md) is a self-contained handoff for a new chat.
Default help is coaching: supply your attempt, failure output and observations;
ask explicitly for a hint, full solution, direct fix or review when desired.

- [Practice guide](docs/practice-guide.md)
- [Explanation template](docs/explanation-template.md)
- [Our review rubric](docs/review-rubric.md)
- [Learner progress template](docs/learner-progress-template.md)
- [Research and source limitations](docs/interview-research.md)

## Deliberate access to hints and solutions

WARNING: instructor materials can reveal answers. Request one hint at a time.
To reveal only E01's first hint without switching this workspace:

```sh
git show solutions:solutions/easy/e01-annotation-reports/hints/01-direction.md
```

To read solution retrieval and evaluation instructions (answer access warning):

```sh
git show solutions:solutions/README.md
```

Those instructions explain exporting one package, testing an attempt with extra
tests and applying a reference patch to a fresh original copy. The example patch
is one valid solution; alternate implementations are judged by behavior and tests.

## Maintenance verification

```sh
python3 -m unittest discover -s scripts -v
```

This checks the attempt helper. Do not interpret intentionally failing starter suites
as infrastructure failures. No perpetually failing CI is configured. The solutions
branch supplies a manual fresh-copy collection verifier, documented in its README.
