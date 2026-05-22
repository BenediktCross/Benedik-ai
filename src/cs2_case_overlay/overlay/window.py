from __future__ import annotations

import time

from PySide6.QtCore import QPointF, Qt, QTimer
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget


class CaseOverlayWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.showFullScreen()
        self._skin_strip: list[str] = []
        self._result_skin: str | None = None
        self._start_ts = 0.0
        self._duration = 4.8
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.update)
        self._timer.start(1000 // 144)

    def start_animation(self, strip: list[str], result_skin: str, duration_seconds: float = 4.8) -> None:
        self._skin_strip = strip
        self._result_skin = result_skin
        self._duration = duration_seconds
        self._start_ts = time.perf_counter()
        self.show()
        self.raise_()

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if self._result_skin:
            self._start_ts = 0.0
            self.update()
        super().mousePressEvent(event)

    def paintEvent(self, event) -> None:  # noqa: N802
        del event
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.fillRect(self.rect(), QColor(3, 6, 10, 180))

        marker_x = self.width() // 2
        painter.fillRect(marker_x - 2, 0, 4, self.height(), QColor(73, 255, 129, 210))

        elapsed = time.perf_counter() - self._start_ts if self._start_ts else self._duration
        progress = min(elapsed / max(self._duration, 0.01), 1.0)
        offset = int((1.0 - progress) * 1400)

        y = self.height() * 0.5
        w, h = 220, 110
        for i, skin in enumerate(self._skin_strip[:30]):
            x = marker_x - offset + i * (w + 14)
            painter.fillRect(x, int(y - h / 2), w, h, QColor(20, 25, 31, 220))
            painter.setPen(QColor(225, 232, 241))
            painter.drawText(QPointF(x + 12, y + 8), skin)

        if progress >= 1.0 and self._result_skin:
            painter.setPen(QColor(141, 255, 169))
            painter.drawText(QPointF(marker_x - 100, y + 95), f"Drop: {self._result_skin}")
