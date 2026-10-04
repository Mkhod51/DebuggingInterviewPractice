"""Worker tick and lifecycle transitions."""
from dataclasses import dataclass
from .handler import RetryableError, PermanentError


@dataclass(frozen=True)
class TickResult:
    processed: tuple
    states: tuple

    def as_dict(self):
        return dict(processed=list(self.processed), states=dict(self.states))


class Worker:
    def __init__(self, repository, handler, clock, policy):
        self.repository = repository
        self.handler = handler
        self.clock = clock
        self.policy = policy

    def _process(self, identifier):
        now = self.clock.now()
        job = self.repository.claim(identifier, now)
        try:
            result = self.handler.execute(job)
        except (RetryableError, PermanentError) as error:
            due = self.policy.due(self.clock.now(), job.attempts) if self.policy.can_retry(job.attempts) else None
            self.repository.fail(identifier, error, due)
        except Exception as error:
            self.repository.fail(identifier, error)
        else:
            self.repository.succeed(identifier, result)
        return self.repository.get(identifier)

    def tick(self):
        ready = self.repository.ready_ids(self.clock.now())
        for identifier in ready:
            self._process(identifier)
        return TickResult(tuple(ready), tuple(self.repository.summary().items()))

    def summary(self):
        return self.repository.summary()
