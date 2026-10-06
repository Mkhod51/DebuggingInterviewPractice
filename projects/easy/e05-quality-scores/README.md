# E05: Quality scores

## Scenario

A review team checks completed annotation work and gives each reviewed item a
quality score. An operations dashboard needs to summarize those reviews both for
each contributor and for the dataset as a whole. Some reviews carry more weight
than others, so a plain average of the scores would not express the required metric.

This application takes review records and produces a report containing overall
and per-contributor summaries, plus a histogram counting reviews in score bands.
It also exports JSON for a caller to display. Scores and weights are supplied
inputs; you do not need to evaluate labels or understand a machine-learning model.

## What the terms mean

- **Review:** a uniquely identified assessment with a contributor ID, a `score`
  and a `weight`. A contributor can have several different reviews.
- **Score:** a value from 0 to 1. Zero is an observed score, not missing data.
- **Weight:** a positive importance multiplier. Weight 2 gives a review twice
  the influence of weight 1; it does not mean there are two review records.
- **Weighted mean:** the sum of each score times its weight, divided by the total
  weight. The same calculation is used for each group and the overall summary.
- **Count versus total weight:** count is the number of review records; total
  weight is the sum of their importance multipliers.
- **No mean:** `None` when there are no reviews. There is no evidence from which
  to calculate a quality value.

## Example of correct behavior

For contributor `alex`, take two reviews: score `0.6` with weight `2`, and score
`0.9` with weight `1`. The summary should have count 2, total weight 3, and mean
`(0.6 * 2 + 0.9 * 1) / 3 = 0.7`. If these are the only reviews in the dataset,
the overall summary has the same values.

An empty collection should instead produce count 0, total weight 0 and mean
`None`, while still allowing report export. Internal means keep their precision;
exported means are rounded to four decimal places. These are expected outputs
to compare with the starter application.

## Behavior contract

- Each review has a finite score in `[0, 1]`, positive finite weight and a unique review ID.
- The quality mean is `sum(score * weight) / sum(weight)`; contributor and overall summaries use the same rule.
- Empty inputs have count zero, total weight zero and mean None. Zero scores participate normally.
- Contributors are sorted by exact identifier. Internal means retain floating-point precision;
  JSON exports round means to four decimal places without altering internal results.
- Inputs and prior report objects must not be mutated. Duplicate review IDs are errors.

## Incident

The dashboard disagrees with manual weighted calculations, and a contributor with no reviews causes report generation to fail.

## Start here

### Codebase map

All application modules are under `src/practice_app/`:

| File | Responsibility |
| --- | --- |
| `models.py` | Review validation, summary values and fixture loading. |
| `scoring.py` | Weighted summaries, contributor grouping and score-band counts. |
| `service.py` | Report assembly, contributor lookup and JSON export. |
| `tests/test_scores.py` | Small review sets with known expected summary values. |
| `fixtures/reviews.json` | Local reviews for a complete report. |

The public entry point is `practice_app.service.generate_report`. Explore the modules and local fixtures
as needed. No network is used by this application or its tests. Tested on Python
3.14.0; metadata allows Python 3.11+, which has not been separately verified.
Practice session target: 20–30 minutes (our design choice).

From this project directory, including a standalone copy:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
python -m pytest -q
python -m pytest -q tests/test_scores.py::test_weighted_mean_uses_total_weight
```

Installation may download pytest and build tools. Starting application test failures
are intentional. Installation, imports and test discovery must work.

Diagnose and correct application behavior, add regression tests and explain your
evidence and findings. You may add tests. Existing tests and expected outputs are
the contract: do not delete, skip, xfail or weaken them to obtain a pass. A passing
suite is evidence, not proof of correctness for every possible input.
