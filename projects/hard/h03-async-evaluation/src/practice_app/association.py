"""Restore input order using completion identity."""
from .models import Result


class AssociationError(ValueError):
    pass


def associate(cases, completions):
    cases, completions = list(cases), list(completions)
    expected_ids = {case.id for case in cases}
    actual_ids = [completion.case_id for completion in completions]
    if len(actual_ids) != len(set(actual_ids)):
        raise AssociationError("Duplicate completion ID")
    if set(actual_ids) != expected_ids:
        raise AssociationError("Missing or unknown completion ID")
    by_id = dict(zip([case.id for case in cases], completions))
    results = []
    for case in cases:
        completion = by_id[case.id]
        if completion.error is not None:
            results.append(Result(case.id, case.expected, None, None, completion.error))
        else:
            results.append(Result(case.id, case.expected, completion.actual,
                                  completion.actual == case.expected, None))
    return tuple(results)


def failures(results):
    return tuple(row for row in results if row.error is not None)


def incorrect(results):
    return tuple(row for row in results if row.error is None and not row.correct)
