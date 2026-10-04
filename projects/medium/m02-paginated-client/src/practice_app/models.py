"""Dataset transport objects and protocol validation."""
from dataclasses import dataclass
from copy import deepcopy


class ProtocolError(ValueError):
    """A local API response violates the pagination contract."""


@dataclass(frozen=True)
class Record:
    id: str
    payload: dict

    @classmethod
    def from_dict(cls, row):
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"]:
            raise ProtocolError("Invalid record ID")
        if not isinstance(row.get("payload"), dict):
            raise ProtocolError("Invalid record payload")
        return cls(row["id"], deepcopy(row["payload"]))

    def as_dict(self):
        return dict(id=self.id, payload=deepcopy(self.payload))


@dataclass(frozen=True)
class Page:
    items: tuple
    next_cursor: str | None

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict) or not isinstance(data.get("items"), list):
            raise ProtocolError("Invalid page items")
        if "next_cursor" not in data:
            raise ProtocolError("Missing next cursor")
        cursor = data["next_cursor"]
        if cursor is not None and not isinstance(cursor, str):
            raise ProtocolError("Invalid cursor")
        return cls(tuple(Record.from_dict(row) for row in data["items"]), cursor)

    def as_dict(self):
        return dict(items=[row.as_dict() for row in self.items], next_cursor=self.next_cursor)
