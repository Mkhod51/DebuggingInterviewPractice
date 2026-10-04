# Working in this repository

Default to coach mode during ordinary practice. Ask for the exercise, attempt path,
failing output and observations when missing. Help the learner test hypotheses;
reveal one hint only when requested. Do not inspect the solutions branch or alter
attempts without an explicit request. Explicit requests for full solutions, direct
fixes, reviews or development override this default.

The initial BUILD_PROMPT.md authorizes building and verifying all fifteen exercises
and instructor packages now, including local branches and regular commits. It does
not authorize pushes, PRs, publication or messages to others. Keep instructor content
outside this checkout and exclusively on the solutions branch. Never merge solutions
into codex/debugging-practice. Do not leak root causes into candidate documentation.

Exercises are independent installed Python packages. Starting application failures
are intentional; import, installation and discovery failures are infrastructure bugs.
Existing tests and README contracts must not be weakened. Preserve learner work.
Read docs/LLM_CONTEXT.md and actual state before helping; do not invent progress.
