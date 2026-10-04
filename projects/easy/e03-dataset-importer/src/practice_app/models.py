"""Imported records and row diagnostics."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Record:
    id: str
    text: str
    weight: float
    label: str

    def as_dict(self):
        return dict(id=self.id, text=self.text, weight=self.weight, label=self.label)


@dataclass(frozen=True)
class Rejection:
    row: int
    reason: str

    def as_dict(self):
        return dict(row=self.row, reason=self.reason)


@dataclass(frozen=True)
class ImportResult:
    records: tuple
    rejected: tuple

    @property
    def accepted_count(self):
        return len(self.records)

    def as_dict(self):
        return dict(records=[row.as_dict() for row in self.records],
                    rejected=[row.as_dict() for row in self.rejected])

    def by_label(self):
        result = {}
        for record in self.records:
            result.setdefault(record.label, []).append(record)
        return result
