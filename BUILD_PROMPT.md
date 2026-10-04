

You are building my Python debugging interview practice repository. Implement the agreed specification below and continue until all 15 exercises, their solution packages, documentation, and verification are complete.

## Context and objective

I am preparing for Scale AI's Software Engineering Intern (Summer 2027), London, debugging interview. The interview description I received says:

> This debugging practical interview question will be hosted in Hackerrank and is available in Python and Typescript. Candidates will navigate a new codebase and debug failing test cases. Candidates will be expected to explain where and why certain parts of the code are not performing as intended in addition to making the proper changes to correct the system.

I have chosen **Python throughout**. I have already approved the structure and solution packaging in this prompt. You are authorized to create the exercises, local Git branches, documentation, helper scripts, and frequent local commits. Do not stop to ask me to approve the plan again. Do not push, publish, create a PR, or message anyone unless I request that separately.

Repository:

```text
/Users/mkhoder/Career/Internship apps /IndividualApps/ScaleAI/InterviewPrep/DebugPractice/DebugPracice
```

At the time this prompt was prepared, the repository was on `main`, with an initial commit and `.gitattributes`. Inspect the actual state before working; preserve any existing user changes. Quote paths correctly because this repository path contains spaces. Read applicable `AGENTS.md` files and follow any relevant installed skills.

The role involves contributor matching, annotation and training-data pipelines, evaluation infrastructure, reliable AI applications, and large-scale data processing. Use those as understandable product settings. The exercises must not require ML expertise or prior knowledge of Scale's internal systems.

## Research basis and limits

The strongest evidence is my interview description above. Public candidate accounts support practicing unfamiliar modular code, failure isolation, tracing dependencies, and communicating under time pressure:

- September 2026 intern schedule reporting a 60-minute Python/TypeScript debugging practical: https://www.reddit.com/r/leetcode/comments/1wif7yz/scale_ai_swe_intern_virtual_onsite_what_to_expect/
- New-grad account describing around 150–200 lines of modular code and using print statements to trace missing model output: https://www.tryexponent.com/experiences/scale-ai-software-engineer-interview-b83485
- Edited candidate account describing a multi-file contributor-assignment debugging exercise: https://prachub.com/interview-experiences/scale-ai-software-engineer-interview-experience-debug-a-real-codebase-then-an-llm-api-round
- Official HackerRank project interview documentation: https://support.hackerrank.com/articles/1769104522-importing-projects-in-hackerrank-interview-

Record this background, with links and an October 4, 2026 research date, in `docs/interview-research.md`. Distinguish direct recruiter information, anecdotal reports from different roles, and our design choices. Verify linked material before making additional source-specific claims. Do not present reported questions, line counts, defect counts, time limits, or our review rubric as official Scale requirements. Build original practice scenarios rather than reproducing reported interview questions.

## Deliverable: exactly 15 independent exercises

Create 5 easy, 5 medium, and 5 hard Python projects:

| ID | Directory | Product setting | General practice focus |
| --- | --- | --- | --- |
| E01 | easy/e01-annotation-reports | Annotation report generator | Filtering, grouping, summaries |
| E02 | easy/e02-task-queue | Task queue | Ordering, eligibility, capacity |
| E03 | easy/e03-dataset-importer | Dataset importer | Parsing, validation, boundaries |
| E04 | easy/e04-contributor-directory | Contributor directory | Lookups, identifiers, optional values |
| E05 | easy/e05-quality-scores | Quality score calculator | Aggregation, empty inputs, numeric behavior |
| M01 | medium/m01-contributor-assignment | Contributor assignment service | Rules and state across modules |
| M02 | medium/m02-paginated-client | Paginated dataset client | API contracts and accumulated results |
| M03 | medium/m03-evaluation-runner | Model evaluation runner | Input/output alignment, metrics |
| M04 | medium/m04-prediction-cache | Cached prediction service | Request identity, cache behavior, mutation |
| M05 | medium/m05-job-worker | Retrying job worker | Failure handling and job lifecycle |
| H01 | hard/h01-contributor-allocation | Contributor allocation pipeline | Interacting constraints, repeated runs |
| H02 | hard/h02-incremental-sync | Incremental data synchronizer | Checkpoints, duplicates, partial failures |
| H03 | hard/h03-async-evaluation | Asynchronous evaluation service | Completion order, failures, result association |
| H04 | hard/h04-model-gateway | Model request gateway | Request tracing through multiple layers |
| H05 | hard/h05-annotation-workflow | Annotation workflow engine | State transitions and component consistency |

Targets, excluding tests and fixtures:

| Difficulty | Application size | Application modules | Intentional defects | Session target |
| --- | --- | --- | --- | --- |
| Easy | 120–220 lines | 2–3 | 1–2 | 20–30 minutes |
| Medium | 220–400 lines | 3–5 | 2–3 | 35–45 minutes |
| Hard | 350–650 lines | 4–7 | 3–5 | 60 minutes |

Treat size ranges as guidelines. Never pad code to reach a count. The number of exercises is exact. Make difficulty come from causal distance, interactions, state, and subtle edge cases, while keeping the code readable. Most fixes should be small once the cause is understood.

## Practice branch structure

Use `codex/debugging-practice` as the practice branch unless the actual repository has an already suitable user-designated branch. Leave the primary workspace on the practice branch when finished.

```text
README.md
AGENTS.md
BUILD_PROMPT.md
docs/
  LLM_CONTEXT.md
  BUILD_STATUS.md
  interview-research.md
  practice-guide.md
  explanation-template.md
  review-rubric.md
  learner-progress-template.md
projects/
  easy/       # E01–E05
  medium/     # M01–M05
  hard/       # H01–H05
scripts/
  start_attempt.py
attempts/     # Gitignored
```

Each project must contain:

```text
README.md
pyproject.toml
src/
  practice_app/
    __init__.py
    ... application modules
tests/
  ... visible tests
fixtures/
  ... relevant local inputs
```

Every exercise must work when copied outside this repository. No shared application imports, shared fixtures, root-only test configuration, or dependency on the helper script. Reusing the package name `practice_app` is fine because each exercise uses its own environment and is tested separately.

Use pytest and standard-library application code wherever practical. Inspect available runtimes and document a tested Python version. Keep dependency configuration minimal, reproducible, and consistent across exercises. Every README must provide exact commands to create an environment, install that exercise, run all tests, and run a selected test. State that the starting test failures are intentional.

Use local fake API/model clients, local repositories, controlled clocks, and deterministic inputs. No paid services, API keys, live model calls, external network access during tests, Docker, database servers, frontend build systems, or GPU requirements. Dependency installation can require network access; exercise execution must not.

## Exercise design requirements

For each exercise, write down the intended behavior and create a correct implementation before introducing deliberate defects. Keep the correct implementation and defect design outside the practice checkout until packaging them on the solutions branch.

Candidate-facing README content:

- A concise product brief explaining what the system does.
- Explicit behavior rules, including the edge-case decisions needed to judge correctness.
- A symptom or incident report that motivates investigation without pointing to the faulty function.
- An entry point and setup/test commands, without giving away the causal path.
- The task: diagnose, correct application code, preserve intended behavior, add regression coverage, and explain the findings.
- Permission to add tests; existing tests and expected outputs are the exercise contract and must not be weakened to obtain a pass.

Candidate-facing source should resemble a small maintained codebase: clear names, reasonable abstractions, ordinary docstrings, and some healthy functionality. No `BUG HERE`, defect-count comments, TODO solutions, stubbed core functions, intentionally misleading documentation, or missing dependencies. Startup, imports, and test discovery must work. Failures must come from behavioral defects, not environmental sabotage.

Include passing and failing visible tests, tests across relevant modules, and at least one end-to-end test per exercise. Use informative behavior-based test names and assertions; do not encode the fix or source location in names. All deliberate defects must be detectable through at least one visible test once masking defects are corrected. Extra solution tests should strengthen confidence and catch incomplete fixes, not reveal undocumented requirements.

Include varied defects across the collection, avoiding fifteen versions of the same off-by-one error. Choose exact defects yourself and keep their descriptions off the practice branch. Hard exercises should include interacting defects, such as a failure that becomes visible only after an earlier one is corrected. Use deterministic events/barriers or controlled fake clients for asynchronous cases, not fragile timing races or real sleeps.

Do not mark intentional failures with `xfail`, skip them, weaken assertions, or supply production code that hardcodes test fixtures. The normal candidate test command must honestly fail initially and pass after a correct solution.

## Solutions branch and precise contents

Create a separate local Git branch named **`solutions`**, as agreed. The `solutions/` directory must exist only on that branch, never in the practice branch's tracked files or working tree. Keep instructor-only temporary material outside the primary workspace as well.

The solutions branch should retain the original buggy projects and add solution packages; do not replace its project source with fixed implementations. This keeps the reference patches applicable and avoids maintaining duplicate application trees. You may use a separate worktree for this branch if helpful. Keep it current by bringing practice-branch changes into the solutions branch only. Never merge the solutions branch back into the practice branch. Preserve any pre-existing branches or worktrees.

Mirror project paths:

```text
solutions/
  README.md
  easy/
    e01-annotation-reports/
      hints/
        01-direction.md
        02-investigation.md
        03-root-cause.md
      explanation.md
      reference.patch
      extra_tests/
        test_regressions.py
      fixtures/                 # Only when needed
      verification.json
  medium/ ...
  hard/ ...
```

Required contents for every exercise:

1. `01-direction.md`: a broad behavior or stage to investigate, without revealing the faulty line. Where several defects exist, organize hints by neutral incident/test grouping.
2. `02-investigation.md`: useful inputs, assertions, log statements, or comparisons that help test a hypothesis.
3. `03-root-cause.md`: the faulty assumption and relevant function, stopping short of supplying the patch.
4. `explanation.md`: every deliberate defect, its symptom, expected behavior, evidence-driven investigation, root cause and location, minimal correction, regression coverage, and a short spoken interview explanation. Explain masking and interactions where relevant. Discuss reasonable alternative fixes.
5. `reference.patch`: an application-code-only patch relative to the documented original exercise version. Paths must be relative to the exercise root. It must pass `git apply --check` in a fresh exercise copy and must not change tests to make them pass.
6. `extra_tests/`: meaningful tests for documented edge cases and plausible incomplete fixes. Supply a clear way to run them against an attempt without overwriting that attempt's source or existing tests.
7. `fixtures/`: only additional data actually used by the extra tests. Make fixture paths work in the documented evaluation workflow.
8. `verification.json`: use one simple schema across projects, recording the project ID, original exercise Git revision, Python/tool versions used, defect IDs, expected baseline failing test node IDs, expected passing behavior, reference-patch checks, and actual verification outcomes. Record genuine results; distinguish application defects from infrastructure errors. Do not copy this spoiler-bearing metadata to the practice branch.

The root `solutions/README.md` must document exact, tested commands for reading one hint at a time without switching the practice workspace, obtaining one solution package, running additional tests against an attempt, and applying a patch to a fresh copy. Warn clearly before revealing answers. The reference patch is an example solution, not the only acceptable implementation: judge alternative fixes by the behavior contract and tests.

## Small attempt helper

Implement `scripts/start_attempt.py` with the standard library. It should accept a project ID, find the corresponding exercise, and copy it into a new directory under `attempts/`, preserving its standalone structure. Exclude virtual environments, caches, build outputs, and other generated files. Print the destination and next setup/test commands.

It must work regardless of the caller's current directory, validate IDs, and refuse to overwrite an existing attempt. Starting another attempt must preserve previous work. Do not implement destructive reset behavior, automatic grading, a custom testing framework, a web dashboard, or an elaborate command-line platform. Test the helper's meaningful behaviors in temporary directories, including unknown IDs and destination collisions.

## Documentation for me and future LLM chats

**`docs/LLM_CONTEXT.md` is a first-class deliverable.** I should be able to paste just this file into a fresh LLM conversation and have it understand the repository, my goal, and how to help. It must be self-contained, not merely links to other files.

Include:

- My interview context, Python choice, exact repository purpose, and the distinction between confirmed information and practice assumptions.
- The 15-project catalog, difficulty targets, directory conventions, and current completion status.
- Tested setup/test commands, branch names, how to start attempts, and how to obtain a hint or solution deliberately.
- A default **coach mode**: ask for my current project, attempt path, failing output, and observations if missing; help me form hypotheses and explain evidence; reveal one hint at a time only when requested; do not silently fix my attempt or inspect solution content.
- How to switch modes explicitly: I can request full solutions, direct fixes, a review, or further exercise development. My explicit request takes precedence over the default coaching behavior.
- How to assess fixes and explanations, preserving the distinction between observed evidence and guesses.
- Clear scope boundaries: intentionally broken application tests are expected; broken installation/imports are not. Passing tests alone do not prove every possible input is correct.
- Instructions to read the actual repo and attempt state when tools are available, and to request relevant snippets/output when they are not. Never imply the new chat already has filesystem access or knows my progress.
- A short editable learner-state block: current exercise, attempt directory, completed exercises, elapsed time, hints used, hypotheses, and next step. Initially mark my progress as unknown/not supplied; do not invent accomplishments.
- Remaining implementation issues if any, with enough detail for another agent to resume. Update this as work progresses and remove stale blockers when resolved.

Keep this context file free of exact defects, patches, failing-line references, and instructor metadata. It can identify solution locations without exposing their contents.

Other docs:

- `README.md`: accessible starting point, full exercise catalog, installation guidance, intentional-failure explanation, attempt workflow, and pointer to the handoff file.
- `AGENTS.md`: distinguish authorized builder work from ordinary coaching; default to coaching during practice; do not inspect solutions or change attempts without an explicit request; do not leak answers into candidate docs. Make clear this build prompt authorizes generating and verifying instructor materials now.
- `docs/BUILD_STATUS.md`: spoiler-free task checklist and actual completion/validation status. Include the latest meaningful commit references, commands checked, known limitations, and next action. Keep it current at task boundaries. Do not store exact defect descriptions here.
- `docs/practice-guide.md`: untimed learning and timed sessions; reproduce, trace, hypothesize, instrument, fix, add coverage, rerun, explain. Recommend a 60-minute full mock without claiming that my duration is confirmed.
- `docs/explanation-template.md`: symptom → expected behavior → hypothesis → evidence → root cause → correction → verification.
- `docs/review-rubric.md`: diagnosis, evidence, correctness, regression coverage, communication, and sensible use of time. Label it our practice rubric, not Scale's official grading.
- `docs/learner-progress-template.md`: fields to track sessions, time, hints used, findings, and lessons. Do not automatically count test runs as completed practice sessions.

## Frequent local commits: approximately two per task

Commit **very regularly**, as each meaningful checkpoint is verified. Do not save all work for a final commit or lump all exercises into one commit. Aim for approximately **two meaningful commits per named task**, usually around 34–40 commits across both branches for the full build. This is a cadence target, not a reason to create empty or artificial commits.

For a typical exercise task:

1. On the practice branch, commit its standalone candidate project, visible tests, fixtures, and brief after verifying its intended baseline behavior.
2. On the solutions branch, commit its hint files, explanation, reference patch, additional tests, and verification record after validating the correction in a fresh copy. Include any instructor tooling/doc updates relevant to that task.

For foundation and final integration tasks, use two similarly meaningful checkpoints. If a task needs a substantive correction after its checkpoints, make another focused commit instead of hiding it in a later unrelated task. Update progress docs alongside the relevant work.

Use human-readable commit messages that describe the actual change, for example:

```text
Add the annotation reports debugging exercise
Document and verify the annotation reports solution
Add safe working copies for practice attempts
Explain how a new chat should coach debugging sessions
Verify all fifteen exercises from fresh copies
```

By "human names," I mean readable commit/task titles. Keep the configured Git author identity; do not impersonate a person or change attribution. Avoid opaque names such as `task-7`, `checkpoint`, or `update`. Stage explicit relevant paths, inspect staged changes, and avoid including unrelated user files. Do not amend or rewrite existing history unless I request it.

Intentional failing application tests are acceptable at a verified exercise checkpoint: verify the known baseline rather than falsely saying its candidate suite passes. Infrastructure and the reference solution must work before you claim verification.

## Execution order and quality gates

1. Inspect repository state, instructions, and available Python tooling. Create a concrete checklist and establish the practice branch and documentation foundation.
2. Build and verify E01, M01, and H01 as pilots. Assess size, navigability, reproducibility, and difficulty against the specification. Adjust them yourself where needed; do not stop waiting for a second plan approval.
3. Finish the remaining exercises, one task at a time, following the frequent-commit cadence.
4. Complete the handoff/coaching docs, helper validation, solution instructions, and whole-repository audit.

For **every** exercise, verify:

- It installs, imports, and discovers tests in its own clean environment outside the repository.
- The original source has both passing tests and the intended failing tests, with no unrelated collection/setup failures.
- Every planted defect is detected, including after earlier masking defects are fixed. Check this by restoring individual defects into the reference implementation or by an equally concrete experiment, not by assumption.
- The patch applies cleanly to the recorded original version.
- The patched copy passes all visible and extra tests.
- Additional tests cover plausible incomplete fixes and adhere to the documented behavior contract.
- Fake clients, clocks, and asynchronous execution are deterministic and isolated across tests.
- Candidate README rules, fixtures, expected results, and solution explanations agree.

For final verification:

- Confirm exactly 5 projects at each difficulty and a matching solution package for all 15.
- Run installation and baseline/reference checks from fresh copies using the commands in the docs.
- Verify the helper, documented hint/solution retrieval commands, and safe patch workflow.
- Audit tracked practice-branch files and working-tree contents for accidental answers or instructor-only material. Solution content must not appear in practice-branch history.
- Do not configure CI to run all buggy suites and fail perpetually. If you add CI, make it explicitly verify expected baselines and reference solutions; otherwise document the manual validation workflow and omit CI.
- Recheck `LLM_CONTEXT.md` and `BUILD_STATUS.md` against the final actual state.
- Leave the main workspace on the practice branch, preserve attempts/user changes, and ensure your intended changes are committed. Report pre-existing dirty files separately if present.

Use appropriate tools and relevant installed skills. Do not spawn subagents unless I subsequently authorize delegation or applicable instructions explicitly require it. Keep progress updates concise, report substantive milestones, and continue autonomously through all fifteen projects. Do not fabricate successful commands, measurements, or validation results.

## Final delivery

Provide a concise summary with clickable paths to the root README and `docs/LLM_CONTEXT.md`, the first setup/attempt commands, both branch names, commit totals for each branch, and the actual verification results. Clearly distinguish intentionally failing starter suites from passing reference solutions. State any remaining limitation honestly. Do not reveal defect locations or solutions in the final response.

Begin implementation now.
