# Build status

Complete as of October 4, 2026. All intended builder changes are committed at the
final integration checkpoints. Learner practice progress is unknown/not supplied.

- [x] Inspect repository, applicable instructions and available Python.
- [x] Establish practice branch and documentation foundation; preserve supplied prompt.
- [x] Build and assess E01, M01, H01 pilots.
- [x] Complete exactly five easy, five medium and five hard standalone projects.
- [x] Package all fifteen solutions exclusively on the solutions branch.
- [x] Verify standalone installs, imports and default/selected test discovery.
- [x] Verify exact expected behavioral baselines and each defect in isolation.
- [x] Check application-only patches and passing visible plus additional tests.
- [x] Confirm additional tests reject isolated incomplete corrections.
- [x] Validate helper, hint access, package export and safe patch/evaluation workflows.
- [x] Audit practice files, working tree and history for accidental instructor content.
- [x] Complete self-contained coaching handoff and learner templates.

## Actual verification

Final fresh-copy audit: **15 isolated environments**, Python **3.14.0**, pytest
**9.0.2**, pip **25.2**; isolated build requirement setuptools **82.0.1**.
Starter suites: **56 passing and 60 expected failing tests** (116 visible tests).
Patched copies: **149 passing visible/additional tests**, zero failures and zero
collection/setup errors. Each deliberate defect was separately restored and detected
by visible tests and additional tests. No skips or xfails were used.

`python3 -m unittest discover -s scripts -v`: **4 passed**. Production helper was
also tested with real E01 content in a temporary repository-shaped copy from another
working directory; a collision and second attempt preserved the earlier work.

Checked commands/workflows:

```sh
python3 scripts/start_attempt.py E01 --name first
python3 -m venv .venv
python -m pip install -e ".[test]"
python -m pytest -q
python -m pytest -q tests/test_reports.py::test_empty_report_is_exportable
git show solutions:solutions/easy/e01-annotation-reports/hints/01-direction.md
git show solutions:solutions/README.md
```

Every exercise's selected README test command was checked. All three hint retrievals
were compared with their original files. Single-package export, original-revision
export, `git apply --check`, patch application, visible tests and extra tests against
both original and fixed copies were tested without overwriting an active attempt.
Dependency installation may use network; the applications use local data and fakes.

Instructor records and the reusable collection verifier are on solutions only:
`solutions/collection-verification.json`, per-package verification.json and
`solutions/verify_collection.py`. No failing-by-design CI was added. Read instructor
instructions deliberately; ordinary coaching must not inspect answers.

## Checkpoints and final state

- Foundation: `430477f`; safe attempts: `6482394`.
- Pilot practice checkpoints: E01 `38eb542`, M01 `fa86867`, H01 `8f34d40`.
- Final project checkpoint: `faeb88d`.
- Coaching handoff checkpoint: `4e3e9d3`.
- Instructor access/verifier checkpoint: `2d1b0db`.
- The final integration commits include this status and the full verification report.
  Obtain their current IDs with `git log -1 --oneline codex/debugging-practice` and
  `git log -1 --oneline solutions`.

There are 19 new practice checkpoints and 17 additional solution checkpoints,
36 new commits across the build (excluding the initial commit). The solutions branch
includes practice history through forward merges; it was never merged into practice.
The primary workspace remains on codex/debugging-practice. main retains the initial
commit. No pushes, PRs, publication or messages to others were made. The pre-existing
untracked BUILD_PROMPT.md was preserved byte-for-byte and included as authorized.
No unrelated user changes or attempts were modified.

## Limitations and next action

Only Python 3.14.0 was exercised; Python 3.11+ metadata does not claim verification
of every supported interpreter. Some application sizes are below the suggested ranges:
easy 105–127, medium 173–216,
hard 283–325 physical source lines (including ordinary
docstrings, blank lines and package initializers, excluding tests/fixtures). We kept
compact implementations rather than padding; module split, state and interaction
targets remain represented. One supplied public account could not be retrieved;
research limitations are documented. Tests support their contracts and do not prove
correctness for every possible input or predict Scale's exact practical.

Remaining builder work: none. Next learner action: choose a project and start an attempt.
