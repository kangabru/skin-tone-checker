from PyQt5.QtCore import QByteArray, Qt, QRectF, QLineF, pyqtSignal, QSize
from PyQt5.QtGui import QFontDatabase, QFont, QPainter, QPainterPath, QColor, QPen, QIcon, QImage, QBrush
from PyQt5.QtWidgets import QPushButton, QApplication, QWidget
from threading import Timer
from typing import Callable
from src.util import GetResourcePath

_ICON_SIZE = 35
_MARKER_SIZE = 50
_WATCH_TIMEOUT = 0.1 # Seconds
_PICK_RADIUS = 5

class ColorPicker(QPushButton):
    colorChanged = pyqtSignal(QColor)

    def __init__(self, getWindowOnTop: Callable[[], bool], setWindowOnTop: Callable[[bool], None]):
        super().__init__()
        self._wasWindowOnTop = False
        self._getWindowOnTop = getWindowOnTop
        self._setWindowOnTop = setWindowOnTop

        self.setIconSize(QSize(_ICON_SIZE, _ICON_SIZE))
        self._setIcon()
        self._marker: QWidget = MarkerWindow()
        self._isWatching = False
        self._timer = None
        self.setToolTip("Click and drag to watch a specific area.")

    def closeEvent(self, event):
        self._marker.close()
        self.stopWatching()
        super().closeEvent(event)

    def _setIcon(self, alt=False):
        self.setIcon(QIcon(GetResourcePath("icon/icon%s.png" % ("_alt" if alt else ""))))

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self._isWatching = not self._isWatching

        if self._isWatching:
            self._startWatching()
        else:
            self.stopWatching()
            self.resetOnTop()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.setCursor(Qt.ArrowCursor)

        if self._isWatching:
            self._wasWindowOnTop = self._getWindowOnTop()
            self._setWindowOnTop(True)
            event.accept() # Stop propagation to main widget so it doesn't reset the on top status
        else:
            self._setIcon()


    def mouseMoveEvent(self, event):
        pos = event.globalPos()
        self._marker.move(pos.x(), pos.y())

    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor if self._isWatching else Qt.SizeAllCursor)

    def leaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)

    def isWatching(self) -> bool:
        return self._isWatching

    def _startWatching(self):
        self.setCursor(Qt.CrossCursor)
        self._setIcon(True)
        self._marker.show()
        self._timer = Timer(_WATCH_TIMEOUT, self._watch)
        self._timer.start()

    def stopWatching(self):
        self._setIcon()
        self._marker.hide()
        self._isWatching = False
        self._timer and self._timer.cancel()

    def resetOnTop(self):
        if self._wasWindowOnTop is not None:
            self._setWindowOnTop(self._wasWindowOnTop)
            self._wasWindowOnTop = None

    def _watch(self):
        if self._isWatching:
            x, y = self._marker.pos().x() + _MARKER_SIZE / 2, self._marker.pos().y() + _MARKER_SIZE / 2
            getAverageColorFromPosition(x, y, self.colorChanged.emit)
            self._startWatching()


class MarkerWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setFixedSize(_MARKER_SIZE, _MARKER_SIZE)
        self._isPressed = False
        self.move(1, 1)
        self.hide()

    def move(self, x, y):
        super().move(x - _MARKER_SIZE / 2, y - _MARKER_SIZE / 2)
        if not self._isPressed: self.press()

    def paintEvent(self, event):
        super().paintEvent(event)
        size, mid = _MARKER_SIZE, _MARKER_SIZE / 2

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        # Clip
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), mid, mid)
        painter.setClipPath(path)

        # Set slight transparent fill to enable click and drag
        if self._isPressed: painter.setBrush(QBrush(QColor(255, 255, 255, 1))) # Fill

        # Draw outline
        painter.setPen(QPen(QColor(0, 174, 255), 8))
        painter.drawRoundedRect(self.rect(), mid, mid)

    def mousePressEvent(self, event):
        self.press()
        self.setCursor(Qt.CrossCursor)

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.SizeAllCursor)

    def mouseMoveEvent(self, event):
        pos = event.globalPos()
        self.move(pos.x(), pos.y())

    def enterEvent(self, event):
        self.setCursor(Qt.SizeAllCursor)
        self.press()

    def leaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        self.release()

    def press(self):
        self._isPressed = True
        self.update()

    def release(self):
        self._isPressed = False
        self.update()



def getAverageColor(event, emit):
    pos = event.globalPos()
    getAverageColorFromPosition(pos.x(), pos.y(), emit)

def getAverageColorFromPosition(x, y, emit):
    window = int(QApplication.desktop().winId())

    r, d = _PICK_RADIUS, 1 + 2 * _PICK_RADIUS
    image = QApplication.primaryScreen().grabWindow(window, x - r, y - r, d, d).toImage()
    rect = image.rect()

    painter = QPainter(image)
    path = QPainterPath()
    path.addRoundedRect(0, 0, d, d, r, r)
    painter.setClipPath(path) # Clip so we don't include the marker pixels
    painter.end()

    emit(_getAverageColorFromImage(image))

def _getAverageColorFromImage(image):
    width, height = image.width(), image.height()
    r, g, b, count = 0, 0, 0, 0

    for w in range(width):
        for h in range(height):
            color = image.pixelColor(w, h)
            _r, _g, _b, _a = color.getRgb()
            if _a < 1: continue # Ignore transparent pixels
            r, g, b = r + _r, g + _g, b + _b
            count += 1

    if count:
        r, g, b = int(r / count), int(g / count), int(b / count)
    return QColor(r, g, b)
