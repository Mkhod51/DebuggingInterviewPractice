# M03: Evaluation runner

## Scenario

A team is checking whether a text-labeling model gives the expected answers on
a known set of examples. For each example, they already have the correct label.
They send examples to the model in batches, compare returned labels with the
expected ones, and produce a report of both answer quality and service reliability.

The model in this exercise is a scripted local object: it returns supplied
predictions rather than learning from data or contacting a provider. Its output
order can differ from input order, and some predictions may fail or be missing.
Your application turns those outputs into an understandable evaluation report.

## What the terms mean

- **Case:** one evaluation example with a unique `id`, input `text` and an
  `expected` label. The expected label is the answer used for comparison.
- **Prediction:** the model's response, tagged with a `case_id`, containing either
  a label value or an operational error.
- **Batch size:** the maximum number of cases sent in one model call.
- **Correct versus incorrect:** a returned label exactly matches, or differs
  from, that case's expected label.
- **Failed case:** no usable prediction was produced. This is different from a
  usable prediction that gave the wrong label.
- **Accuracy:** correct predictions divided by successfully scored cases.
- **Coverage:** successfully scored cases divided by all input cases, including
  those whose predictions failed. It shows how much of the evaluation could be scored.
- **Protocol error:** duplicate or unknown prediction IDs, which make the model
  response invalid as an evaluation result.

## Example of correct behavior

Consider four cases. Three return usable labels: two match their expected labels
and one does not. The fourth returns an `offline` error. The report should record
two correct cases, one incorrect case and one failed case. Accuracy is `2/3`,
while coverage is `3/4`. The failure has no correctness value (`correct=None`).

Each result still belongs to its original case, and the report lists results in
input order even if the predictions arrived in another order. With batch size 2,
four cases require two calls of two cases each. These are the intended results
against which to evaluate the starter implementation.

## Behavior contract

- Cases have unique exact IDs, input text and expected labels. Predictions may arrive in any order.
- Associate by case ID and preserve original case order in results. Missing outputs become errors.
- Duplicate or unknown output IDs are protocol errors; a run produces no report on protocol failure.
- A prediction can contain either a value or an error, never both. Successful label matching is exact.
- Accuracy is correct / successfully scored cases; failed cases are excluded from that denominator.
- Coverage is scored / total. Empty runs and all-error runs have accuracy None; empty coverage is 0.
- Positive batch_size limits each local model call. No network or real model is involved.

## Incident

Some examples are marked incorrect despite the model returning their expected labels. Accuracy also changes when operational failures are added.

## Start here

### Codebase map

All application modules are under `src/practice_app/`:

| File | Responsibility |
| --- | --- |
| `models.py` | Cases, predictions, per-case results and fixture loading. |
| `model.py` | Local model implementations and recorded batch calls. |
| `metrics.py` | Prediction association, protocol checks and aggregate metrics. |
| `service.py` | Batch orchestration and report export. |
| `tests/test_evaluation.py` | Expected association, batching and metric behavior. |
| `fixtures/evaluation.json` | Cases and scripted predictions for a local run. |

The public entry point is `practice_app.service.EvaluationRunner.run`. Explore the modules and local fixtures
as needed. No network is used by this application or its tests. Tested on Python
3.14.0; metadata allows Python 3.11+, which has not been separately verified.
Practice session target: 35–45 minutes (our design choice).

From this project directory, including a standalone copy:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
python -m pytest -q
python -m pytest -q tests/test_evaluation.py::test_out_of_order_predictions_match_their_cases
```

Installation may download pytest and build tools. Starting application test failures
are intentional. Installation, imports and test discovery must work.

Diagnose and correct application behavior, add regression tests and explain your
evidence and findings. You may add tests. Existing tests and expected outputs are
the contract: do not delete, skip, xfail or weaken them to obtain a pass. A passing
suite is evidence, not proof of correctness for every possible input.
