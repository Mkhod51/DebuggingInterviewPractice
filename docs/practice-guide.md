# Practice guide

Start untimed. Read the product brief and behavior contract, install just that project,
and run its entire suite. Save the initial output. Identify a small failing case and
compare it with a passing one. Imports and discovery must work; application failures
are intentional. Fix source behavior while preserving every existing assertion.

Trace one request through the public entry point and relevant modules. Follow data
identity, ordering, intermediate values and state changes. State a hypothesis and
predict what a log or assertion should show before adding instrumentation. Prefer a
small deterministic input to speculative edits. Keep observations separate from guesses.

After a correction, rerun the reproduction and full suite. Add a regression for a
nearby boundary, repeated request, alternate ordering or failure path that could expose
an incomplete fix. Remove noisy instrumentation unless it serves the application.
Explain the cause in ordinary terms, then describe the correction and what you verified.
Tests provide evidence within their coverage; they are not proof for every input.

For timed sessions, use 20–30 minutes for easy, 35–45 for medium and 60 for a hard
full mock. These are our targets, not official Scale durations. In a 60-minute mock,
spend roughly 5 minutes reproducing, 10 reading/tracing, 25 on hypotheses and fixes,
10 on regression/full-suite checks and 10 explaining. Adjust based on evidence;
don't rush an untested guess to fit the schedule. Explain remaining uncertainty aloud.

Use a fresh attempt name each session. Keep earlier work. Request one hint only when
needed and record its level and time. After the session, deliberately compare with a
reference only if desired, then record lessons in the learner progress template.
Never count builder verification or automatic test runs as learner accomplishments.
