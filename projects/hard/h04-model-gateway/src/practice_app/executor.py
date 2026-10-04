"""Transport retry and fallback execution."""
from dataclasses import dataclass
from .transport import TransientError, PermanentError
from .protocol import encode, decode


@dataclass(frozen=True)
class Outcome:
    model: str
    output: str | None
    error: str | None


class Executor:
    def __init__(self, transport, max_attempts=2):
        if max_attempts <= 0:
            raise ValueError("Attempt budget must be positive")
        self.transport = transport
        self.max_attempts = max_attempts

    def _model(self, request, model, trace):
        for attempt in range(1, self.max_attempts+1):
            trace.record("send", model, attempt)
            try:
                response = self.transport.send(model, encode(request, model))
                output = decode(request, model, response)
            except (TransientError, PermanentError) as error:
                trace.record("transient", model, attempt, str(error))
                if attempt == self.max_attempts:
                    return Outcome(model, None, str(error)), True
            except Exception as error:
                trace.record("failed", model, attempt, str(error))
                return Outcome(model, None, str(error)), False
            else:
                trace.record("success", model, attempt)
                return Outcome(model, output, None), False
        raise RuntimeError("Unreachable attempt loop")

    def execute(self, request, selection, trace):
        outcome, exhausted = self._model(request, selection.primary, trace)
        if exhausted and selection.fallback is not None:
            trace.record("fallback", selection.fallback)
            outcome, _ = self._model(request, selection.fallback, trace)
        return outcome
