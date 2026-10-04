"""Request and result values at the gateway boundary."""
from copy import deepcopy
from dataclasses import dataclass, field
import json


@dataclass(frozen=True)
class Request:
    request_id: str
    tenant: str
    text: str
    model: str | None = None
    options: dict = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.request_id, str) or not self.request_id:
            raise ValueError("Request ID required")
        if not isinstance(self.tenant, str) or not self.tenant or not isinstance(self.text, str):
            raise ValueError("Invalid tenant or text")
        if self.model is not None and (not isinstance(self.model, str) or not self.model):
            raise ValueError("Invalid model")
        if not isinstance(self.options, dict):
            raise ValueError("Options must be an object")
        json.dumps(self.options, allow_nan=False)
        object.__setattr__(self, "options", deepcopy(self.options))

    @classmethod
    def from_dict(cls, data):
        return cls(**deepcopy(data))

    def as_dict(self):
        return dict(request_id=self.request_id, tenant=self.tenant, text=self.text,
                    model=self.model, options=deepcopy(self.options))


@dataclass(frozen=True)
class Result:
    request_id: str
    model: str | None
    output: str | None
    error: str | None
    trace: tuple

    @property
    def ok(self):
        return self.error is None

    def as_dict(self):
        return dict(request_id=self.request_id, model=self.model, output=self.output,
                    error=self.error, ok=self.ok, trace=[event.as_dict() for event in self.trace])

    def to_json(self):
        return json.dumps(self.as_dict(), sort_keys=True)
