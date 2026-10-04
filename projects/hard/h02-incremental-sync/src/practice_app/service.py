"""Fixture assembly and portable sync reports."""
import json
from .models import load_events
from .source import EventSource
from .store import Store
from .synchronizer import Synchronizer
from .audit import progress, revisions, deleted_ids


def synchronizer_from_file(path, batch_size=2):
    return Synchronizer(EventSource(load_events(path)), Store(), batch_size)


def report(synchronizer):
    return dict(records=synchronizer.store.records(), progress=progress(synchronizer).as_dict(),
                revisions=revisions(synchronizer.store), deleted=list(deleted_ids(synchronizer.store)))


def export_json(synchronizer):
    return json.dumps(report(synchronizer), sort_keys=True)
