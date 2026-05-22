from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class AppConfig:
    window_title: str = "CS2 Case Overlay"
    target_resolution: tuple[int, int] = (2560, 1440)
    fps_target: int = 144
    assets_root: Path = Path("src/cs2_case_overlay/data")
    cases_json: Path = Path("src/cs2_case_overlay/data/cases.json")
    skins_dir: Path = Path("src/cs2_case_overlay/data/skins")
    skip_key: str = "MouseLeft"
    animation_duration_ms: int = 4800
