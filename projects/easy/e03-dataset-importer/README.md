# E03: Dataset importer

## Scenario

A data team receives a CSV file containing text examples from another system.
Before those examples can be used, the team needs to turn each row into a validated
record. Files may contain a mixture of usable rows and mistakes, so one bad row
should not discard all the good work in the file.

This importer accepts CSV text or a local file and returns two collections:
accepted records and rejected-row diagnostics. A person can use the diagnostics
to correct the source file. The application also supports JSON export; it does
not upload records or train a model.

## What the terms mean

- **Record:** one text example with an `id`, `text`, numeric `weight` and `label`.
- **ID:** an external reference, stored as text. An ID that looks like a number
  still identifies a record; it is not a quantity to calculate with.
- **Weight:** a relative importance value in `(0, 1]` carried into the imported
  record. The importer validates it but does not compute a score from it.
- **Label:** an optional category. An absent value uses `unlabeled`; an explicitly
  empty value is preserved as an empty string.
- **Quoted CSV field:** a field that may contain commas or line breaks as part
  of its value. One logical CSV record can therefore span several physical lines.
- **Diagnostic:** a rejected logical row number and a reason. The header is row 1,
  so the first data record is row 2.

## Example of correct behavior

Given this CSV, with no optional label column:

```csv
id,text,weight
001,"hello, world",0.5
002,another example,1
003,invalid example,0
```

The result should contain records `001` and `002`, both labeled `unlabeled`.
The first record's text is exactly `hello, world`, and its weight is `0.5`.
Logical row 4 is rejected because weight zero is outside the allowed range.
The import still returns the two valid records. By contrast, a file with no
`weight` header fails as a whole because its required structure is missing.
These are expected results, not a claim that the starter already produces them.

## Behavior contract

- Required headers: `id`, `text`, `weight`; an optional `label` header is supported.
- IDs are stripped of outer whitespace but otherwise preserved, including leading zeroes.
- Text is preserved exactly, including commas and newlines inside quoted CSV fields; empty text is invalid.
- Weight is a finite number in `(0, 1]`. Invalid rows are rejected without stopping other rows.
- Duplicate accepted IDs are rejected; a rejected row does not reserve its ID.
- Missing label values become `unlabeled`; explicitly empty labels stay empty.
- Header errors fail the entire import. Diagnostic row numbers count logical records, starting at 2.

## Incident

Imported record identifiers no longer match external references, and text containing quoted line breaks loses formatting.

## Start here

### Codebase map

All application modules are under `src/practice_app/`:

| File | Responsibility |
| --- | --- |
| `models.py` | Accepted records, rejection diagnostics and import result objects. |
| `parser.py` | CSV reading, header checks and individual record validation. |
| `service.py` | Whole-import coordination, duplicate checks, file loading and export. |
| `tests/test_importer.py` | Input text and expected accepted/rejected records. |
| `fixtures/input.csv` | A small example file containing valid and invalid data. |

The public entry point is `practice_app.service.import_text`. Explore the modules and local fixtures
as needed. No network is used by this application or its tests. Tested on Python
3.14.0; metadata allows Python 3.11+, which has not been separately verified.
Practice session target: 20–30 minutes (our design choice).

From this project directory, including a standalone copy:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
python -m pytest -q
python -m pytest -q tests/test_importer.py::test_identifiers_preserve_leading_zeroes
```

Installation may download pytest and build tools. Starting application test failures
are intentional. Installation, imports and test discovery must work.

Diagnose and correct application behavior, add regression tests and explain your
evidence and findings. You may add tests. Existing tests and expected outputs are
the contract: do not delete, skip, xfail or weaken them to obtain a pass. A passing
suite is evidence, not proof of correctness for every possible input.
