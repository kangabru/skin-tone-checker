from PyQt5.QtCore import QByteArray, Qt, QRectF, QLineF, pyqtSignal, QSize
from PyQt5.QtGui import QFontDatabase, QFont, QPainter, QPainterPath, QColor, QPen, QIcon
from PyQt5.QtWidgets import QPushButton, QApplication, QWidget
from threading import Timer
from typing import Callable

_ICON_SIZE = 35
_MARKER_SIZE = 50
_WATCH_TIMEOUT = 0.1 # Seconds

class ColorPicker(QPushButton):
    colorChanged = pyqtSignal(QColor)

    def __init__(self, forceWindowOnTop: Callable[[bool], None]):
        super().__init__()
        self._forceWindowOnTop = forceWindowOnTop
        self.setIconSize(QSize(_ICON_SIZE, _ICON_SIZE))
        self._setIcon()
        self._marker: QWidget = MarkerWindow()
        self._isWatching = False
        self._timer = None

    def closeEvent(self, event):
        self._marker.close()
        self._stopWatching()
        super().closeEvent(event)

    def _setIcon(self, alt=False):
        self.setIcon(QIcon("icon/icon%s.png" % ("_alt" if alt else "")))

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self._isWatching = not self._isWatching

        if self._isWatching:
            self.setCursor(Qt.CrossCursor)
            self._setIcon(True)
            self._marker.show()
            self._startWatching()
        else:
            self._setIcon()
            self._marker.hide()
            self._stopWatching()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.setCursor(Qt.ArrowCursor)

        if self._isWatching:
            self._forceWindowOnTop(True)
        else:
            self._setIcon()

    def mouseMoveEvent(self, event):
        pos = event.globalPos()
        self._marker.move(pos.x(), pos.y())

    def isWatching(self) -> bool:
        return self._isWatching

    def _startWatching(self):
        self._timer = Timer(_WATCH_TIMEOUT, self._watch)
        self._timer.start()

    def _stopWatching(self):
        self._isWatching = False
        self._timer and self._timer.cancel()
        self._forceWindowOnTop(False)

    def _watch(self):
        if self._isWatching:
            x, y = self._marker.pos().x(), self._marker.pos().y()
            getAverageColorFromPosition(x, y, self.colorChanged.emit)
            self._startWatching()


class MarkerWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setFixedSize(_MARKER_SIZE, _MARKER_SIZE)
        self.move(1, 1)
        self.hide()

    def move(self, x, y):
        super().move(x - _MARKER_SIZE / 2, y - _MARKER_SIZE / 2)

    def paintEvent(self, event):
        super().paintEvent(event)
        size, mid = _MARKER_SIZE, _MARKER_SIZE / 2

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        # Clip
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), mid, mid)
        painter.setClipPath(path)

        # Draw cross hairs
        marker_color = QColor(0, 174, 255)
        painter.setPen(QPen(marker_color, 4))
        painter.drawLines(QLineF(mid, 0, mid, size), QLineF(0, mid, size, mid))

        # Draw outline
        painter.setPen(QPen(marker_color, 8))
        painter.drawRoundedRect(self.rect(), mid, mid)


def getAverageColor(event, emit):
    pos = event.globalPos()
    getAverageColorFromPosition(pos.x(), pos.y(), emit)

def getAverageColorFromPosition(x, y, emit):
    image = QApplication.primaryScreen().grabWindow(
        int(QApplication.desktop().winId()),
        x - 6, y - 6, 13, 13).toImage()
    emit(_getAverageColorFromImage(image))

def _getAverageColorFromImage(image):
    width, height = image.width(), image.height()
    r, g, b, count = 0, 0, 0, 0

    for w in range(width):
        for h in range(height):
            color = image.pixelColor(w, h)
            _r, _g, _b, _ = color.getRgb()
            r, g, b = r + _r, g + _g, b + _b
            count += 1

    if count:
        r, g, b = int(r / count), int(g / count), int(b / count)
    return QColor(r, g, b)
