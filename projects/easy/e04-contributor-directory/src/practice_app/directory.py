"""Exact ID and normalized email indexes."""
from .models import normalize_email


class Directory:
    def __init__(self, contributors):
        contributors = list(contributors)
        self._by_id = {row.id.casefold(): row for row in contributors}
        self._by_email = {normalize_email(row.email): row for row in contributors}
        if len(self._by_id) != len(contributors):
            raise ValueError("Duplicate contributor ID")
        if len(self._by_email) != len(contributors):
            raise ValueError("Duplicate email")

    def get(self, identifier):
        return self._by_id.get(identifier)

    def find_email(self, email):
        return self._by_email.get(normalize_email(email))

    def all(self):
        return sorted(self._by_id.values(), key=lambda row: row.id)

    def search(self, text):
        needle = text.casefold()
        return [row for row in self.all() if row.active and needle in row.name.casefold()]

    def __len__(self):
        return len(self._by_id)

    def export(self):
        return [row.as_dict() for row in self.all()]
