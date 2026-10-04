"""Latest-event consistency and operational workflow summaries."""
from dataclasses import dataclass
from .models import STATES


@dataclass(frozen=True)
class Audit:
    state_counts: tuple
    events: int
    problems: tuple

    @property
    def consistent(self):
        return not self.problems

    def as_dict(self):
        return dict(states=dict(self.state_counts), events=self.events,
                    problems=list(self.problems), consistent=self.consistent)


def inspect(store):
    counts = {state: 0 for state in sorted(STATES)}
    latest = {}
    versions = {}
    problems = []
    for event in store.events():
        key = (event.task_id, event.version)
        if key in versions:
            problems.append("duplicate event version: " + event.task_id)
        versions[key] = event
        previous = latest.get(event.task_id)
        if previous is not None and event.version != previous.version+1:
            problems.append("nonsequential events: " + event.task_id)
        latest[event.task_id] = event
    for item in store.all():
        counts[item.state] += 1
        event = latest.get(item.id)
        if event is not None and (event.version != item.version or event.state != item.state):
            problems.append("latest event differs: " + item.id)
    return Audit(tuple(counts.items()), len(store.events()), tuple(problems))


def timeline(store, identifier):
    return tuple((event.version, event.action, event.state) for event in store.events(identifier))
