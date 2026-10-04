"""In-memory prediction cache with explicit expiry."""
from dataclasses import dataclass
from copy import deepcopy


@dataclass(frozen=True)
class Entry:
    value: dict
    expires_at: float


class Cache:
    def __init__(self, clock, ttl=10):
        if ttl <= 0:
            raise ValueError("TTL must be positive")
        self.clock = clock
        self.ttl = ttl
        self._entries = {}

    def get(self, request):
        key = request.key()
        entry = self._entries.get(key)
        if entry is None:
            return None
        if not self.clock.now() <= entry.expires_at:
            del self._entries[key]
            return None
        return entry.value

    def put(self, request, value):
        self._entries[request.key()] = Entry(deepcopy(value), self.clock.now()+self.ttl)

    def invalidate_model(self, model):
        keys = [key for key in self._entries if key[0] == model]
        for key in keys:
            del self._entries[key]
        return len(keys)

    def clear(self):
        count = len(self._entries)
        self._entries.clear()
        return count

    def __len__(self):
        return len(self._entries)

    def prune(self):
        keys = [key for key, entry in self._entries.items() if self.clock.now() >= entry.expires_at]
        for key in keys:
            del self._entries[key]
        return len(keys)
