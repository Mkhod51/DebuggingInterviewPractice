# Interview research

Research date: October 4, 2026. This repository contains original practice scenarios.

## Direct information supplied by the learner

The learner is preparing for Scale AI's Software Engineering Intern (Summer 2027),
London, and chose Python. Their interview description says the practical is hosted
in HackerRank, supports Python and TypeScript, and asks candidates to navigate an
unfamiliar codebase, debug failing cases and explain incorrect behavior and fixes.
This description is the strongest evidence. It does not confirm their time limit,
code size, defect count, specific questions or grading rubric.

## Public accounts (anecdotal)

- [Intern schedule on Reddit](https://www.reddit.com/r/leetcode/comments/1wif7yz/scale_ai_swe_intern_virtual_onsite_what_to_expect/):
  the retrieved post lists a 60-minute debugging practical with Python or TypeScript.
  The learner supplied a September 2026 attribution, but the retrieved page shows
  a relative timestamp; that month was not independently verified. Another person's
  schedule is not confirmation of this learner's schedule.
- [New-grad account supplied via Exponent](https://www.tryexponent.com/experiences/scale-ai-software-engineer-interview-b83485):
  retrieval redirected to aced.io and could not be accessed. The supplied summary
  mentions modular code, roughly 150–200 lines and print-based tracing; these details
  were not independently verified and are not used as requirements.
- [Edited PracHub account](https://prachub.com/interview-experiences/scale-ai-software-engineer-interview-experience-debug-a-real-codebase-then-an-llm-api-round):
  the accessible page describes a software engineer interview in March 2026,
  published August 24, 2026, and identifies itself as curated and edited. It describes
  navigating several files under time pressure. Different role, edited anecdote:
  useful motivation for modular practice, not an official interview specification.

## Platform documentation

[HackerRank: importing projects](https://support.hackerrank.com/articles/1769104522-importing-projects-in-hackerrank-interview-)
was accessible. It describes project import and a candidate IDE in which files can
be explored and the project run. It does not establish Scale's project contents,
Python dependency availability or interview rules. Local pytest practice is our
choice, not a claim about the exact hosted environment.

## Our design choices

Fifteen exercises in three difficulties, small readable fixes, local fake clients,
controlled time, visible tests and separate solutions develop reproducibility,
failure isolation, dependency tracing and spoken explanations. Sizes, defect counts,
20–30 / 35–45 / 60-minute targets and the review rubric are practice design choices.
No ML expertise, internal Scale knowledge or leaked interview question is required.
