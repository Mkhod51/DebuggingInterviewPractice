"""Gate-controlled local predictions and task observation."""
import asyncio
from copy import deepcopy


class ModelFailure(RuntimeError):
    pass


class ControlledModel:
    def __init__(self, outcomes, automatic=False):
        self._outcomes = deepcopy(outcomes)
        self._gates = {id: asyncio.Event() for id in outcomes}
        if automatic:
            for gate in self._gates.values():
                gate.set()
        self._started = asyncio.Queue()
        self._finished = asyncio.Queue()
        self._calls = []
        self._cancelled = []
        self._active = 0
        self._peak = 0

    async def predict(self, case):
        if case.id not in self._gates:
            raise ModelFailure("Missing local response")
        self._calls.append(case.id)
        self._active += 1
        self._peak = max(self._peak, self._active)
        self._started.put_nowait(case.id)
        try:
            await self._gates[case.id].wait()
            outcome = self._outcomes[case.id]
            if "error" in outcome:
                raise ModelFailure(outcome["error"])
            return outcome["value"]
        except asyncio.CancelledError:
            self._cancelled.append(case.id)
            raise
        finally:
            self._active -= 1
            self._finished.put_nowait(case.id)

    def release(self, identifier):
        self._gates[identifier].set()

    def release_all(self):
        for gate in self._gates.values():
            gate.set()

    async def next_started(self):
        return await self._started.get()

    async def next_finished(self):
        return await self._finished.get()

    @property
    def active(self):
        return self._active

    @property
    def peak(self):
        return self._peak

    @property
    def calls(self):
        return list(self._calls)

    @property
    def cancelled(self):
        return list(self._cancelled)

    def summary(self):
        return dict(calls=len(self._calls), active=self._active, peak=self._peak,
                    cancelled=len(self._cancelled))
