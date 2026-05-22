from __future__ import annotations

import asyncio
from dataclasses import dataclass

from cs2_case_overlay.core.bus import AsyncEventBus
from cs2_case_overlay.core.events import CaseOpenStarted, CaseResultDetected, Event, EventType


@dataclass(slots=True)
class DetectionState:
    active_case: str | None = None


class Cs2DetectionService:
    """External read-only detector placeholder.

    Production setup should only perform passive memory reads and must not write
    to game memory, inject DLLs, or hook the renderer.
    """

    def __init__(self, event_bus: AsyncEventBus) -> None:
        self._event_bus = event_bus
        self._state = DetectionState()
        self._running = False

    async def run(self) -> None:
        self._running = True
        while self._running:
            await asyncio.sleep(0.005)

    async def simulate_case_open(self, case_id: str, skin_id: str) -> None:
        await self._event_bus.publish(
            Event(EventType.CASE_OPEN_STARTED, CaseOpenStarted(case_id=case_id))
        )
        await asyncio.sleep(0.3)
        await self._event_bus.publish(
            Event(EventType.CASE_RESULT_DETECTED, CaseResultDetected(case_id=case_id, skin_id=skin_id))
        )

    def stop(self) -> None:
        self._running = False
