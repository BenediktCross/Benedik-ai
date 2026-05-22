from __future__ import annotations

import asyncio
import random
import sys

from PySide6.QtWidgets import QApplication

from cs2_case_overlay.assets.manager import AssetManager
from cs2_case_overlay.config import AppConfig
from cs2_case_overlay.core.bus import AsyncEventBus
from cs2_case_overlay.core.events import CaseResultDetected, Event, EventType
from cs2_case_overlay.detection.memory_reader import Cs2DetectionService
from cs2_case_overlay.overlay.window import CaseOverlayWindow


class AppController:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.bus = AsyncEventBus()
        self.assets = AssetManager(config.cases_json, config.skins_dir)
        self.detector = Cs2DetectionService(self.bus)
        self.overlay = CaseOverlayWindow()

    async def on_result(self, event: Event) -> None:
        if not isinstance(event.payload, CaseResultDetected):
            return
        pool = self.assets.skins_for_case(event.payload.case_id)
        if not pool:
            return
        strip = [random.choice(pool) for _ in range(80)]
        strip[-1] = event.payload.skin_id
        self.overlay.start_animation(strip=strip, result_skin=event.payload.skin_id)

    async def run(self) -> None:
        self.assets.load()
        self.bus.subscribe(EventType.CASE_RESULT_DETECTED, self.on_result)
        await self.detector.simulate_case_open("dreams_and_nightmares", "ak47_nightwish")
        await self.detector.run()


def main() -> None:
    app = QApplication(sys.argv)
    controller = AppController(AppConfig())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(controller.run())

    timer = app.startTimer(8)

    def _tick(_: object) -> None:
        loop.call_soon(loop.stop)
        loop.run_forever()

    app.timerEvent = _tick  # type: ignore[method-assign]
    app.exec()
    app.killTimer(timer)


if __name__ == "__main__":
    main()
