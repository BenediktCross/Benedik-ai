from __future__ import annotations

import json
from pathlib import Path

from PySide6.QtGui import QPixmap


class AssetManager:
    def __init__(self, cases_path: Path, skins_dir: Path) -> None:
        self._cases_path = cases_path
        self._skins_dir = skins_dir
        self._cases: dict[str, list[str]] = {}
        self._cache: dict[str, QPixmap] = {}

    def load(self) -> None:
        self._cases = json.loads(self._cases_path.read_text(encoding="utf-8"))
        for skin_id in {skin for skins in self._cases.values() for skin in skins}:
            img = self._skins_dir / f"{skin_id}.png"
            if img.exists():
                self._cache[skin_id] = QPixmap(str(img))

    def skins_for_case(self, case_id: str) -> list[str]:
        return self._cases.get(case_id, [])

    def skin_image(self, skin_id: str) -> QPixmap | None:
        return self._cache.get(skin_id)
