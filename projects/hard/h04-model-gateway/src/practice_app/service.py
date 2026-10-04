"""Gateway entry point and fixture composition."""
import json
from pathlib import Path
from .models import Request, Result
from .routing import Router, Route, RoutingError
from .transport import FakeTransport
from .tracing import Trace
from .executor import Executor


class Gateway:
    def __init__(self, router, executor):
        self.router = router
        self.executor = executor

    def handle(self, request):
        trace = Trace(request.request_id)
        trace.record("received")
        try:
            selection = self.router.select(request)
        except RoutingError as error:
            trace.record("rejected", detail=str(error))
            return Result(request.request_id, None, None, str(error), trace.events())
        trace.record("routed", selection.primary)
        outcome = self.executor.execute(request, selection, trace)
        trace.record("finished", outcome.model)
        return Result(request.request_id, outcome.model, outcome.output, outcome.error, trace.events())

    def handle_dict(self, data):
        return self.handle(Request.from_dict(data))


def gateway_from_file(path):
    data = json.loads(Path(path).read_text())
    router = Router({tenant: Route.from_dict(row) for tenant, row in data["routes"].items()})
    transport = FakeTransport(data.get("scripts"))
    gateway = Gateway(router, Executor(transport, data.get("max_attempts", 2)))
    return gateway, [Request.from_dict(row) for row in data["requests"]]
