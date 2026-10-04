"""Deterministic local model response construction."""
from copy import deepcopy


class ModelError(RuntimeError):
    pass


class FakeModel:
    def __init__(self):
        self._calls = []
        self._fail_next = False

    def fail_next(self):
        self._fail_next = True

    def predict(self, request):
        self._calls.append(request.as_dict())
        if self._fail_next:
            self._fail_next = False
            raise ModelError("Local model unavailable")
        return dict(model=request.model, version=request.version,
                    prediction=request.text.upper(), options=deepcopy(request.options),
                    details={"tokens": request.text.split()})

    @property
    def calls(self):
        return deepcopy(self._calls)

    def reset_calls(self):
        self._calls.clear()
