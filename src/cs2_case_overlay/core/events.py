from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class EventType(Enum):
    CASE_OPEN_STARTED = auto()
    CASE_RESULT_DETECTED = auto()
    OVERLAY_FINISHED = auto()


@dataclass(slots=True)
class CaseOpenStarted:
    case_id: str


@dataclass(slots=True)
class CaseResultDetected:
    case_id: str
    skin_id: str


@dataclass(slots=True)
class Event:
    type: EventType
    payload: CaseOpenStarted | CaseResultDetected | None = None
