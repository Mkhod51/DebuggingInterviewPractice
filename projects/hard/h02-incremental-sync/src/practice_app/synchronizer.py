"""Batch processing with recovery across stream and storage boundaries."""
from dataclasses import dataclass
from .models import BatchResult


class ApplyFailure(RuntimeError):
    pass


@dataclass(frozen=True)
class RunResult:
    batches: tuple
    consumed: int
    applied: int

    def as_dict(self):
        return dict(batches=[batch.as_dict() for batch in self.batches],
                    consumed=self.consumed, applied=self.applied)


class Synchronizer:
    def __init__(self, source, store, batch_size=2):
        if batch_size <= 0:
            raise ValueError("Batch size must be positive")
        self.source = source
        self.store = store
        self.batch_size = batch_size

    def step(self, fail_event=None):
        events = self.source.fetch(self.store.checkpoint, self.batch_size)
        if not events:
            return BatchResult(0, 0, self.store.checkpoint)
        self.store.checkpoint = events[-1].cursor
        before = self.store.snapshot()
        try:
            applied = 0
            for event in events:
                if event.id == fail_event:
                    raise ApplyFailure("Local application interrupted")
                applied += self.store.apply(event)
            self.store.checkpoint = events[-1].cursor
        except Exception:
            self.store.restore(before)
            raise
        return BatchResult(len(events), applied, self.store.checkpoint)

    def run(self, fail_event=None):
        batches = []
        while True:
            result = self.step(fail_event)
            if result.consumed == 0:
                break
            batches.append(result)
        return RunResult(tuple(batches), sum(row.consumed for row in batches),
                         sum(row.applied for row in batches))
