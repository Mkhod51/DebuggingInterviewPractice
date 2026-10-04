"""Prediction orchestration and local fixture workflow."""
import json
from pathlib import Path
from .models import Request, Clock, Stats
from .cache import Cache
from .backend import FakeModel


class PredictionService:
    def __init__(self, backend, cache):
        self.backend = backend
        self.cache = cache
        self._hits = 0
        self._misses = 0
        self._backend_calls = 0

    def predict(self, model, version, text, options=None):
        request = Request(model, version, text, options or {})
        cached = self.cache.get(request)
        if cached is not None:
            self._hits += 1
            return cached
        self._misses += 1
        self._backend_calls += 1
        value = self.backend.predict(request)
        self.cache.put(request, value)
        return value

    def stats(self):
        return Stats(self._hits, self._misses, self._backend_calls)

    def invalidate_model(self, model):
        return self.cache.invalidate_model(model)


def service_from_file(path):
    data = json.loads(Path(path).read_text())
    clock = Clock(data.get("now", 0))
    backend = FakeModel()
    service = PredictionService(backend, Cache(clock, data.get("ttl", 10)))
    return service, clock, data["requests"]
