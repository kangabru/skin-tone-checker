from PyQt5.QtCore import QByteArray, Qt, QRectF, QLineF, pyqtSignal, QSize
from PyQt5.QtGui import QFontDatabase, QFont, QPainter, QPainterPath, QColor, QPen, QIcon
from PyQt5.QtWidgets import QPushButton, QApplication, QWidget


class MarkerWindow(QWidget):
    size = 50

    def __init__(self, *args, **kwargs):
        super(MarkerWindow, self).__init__(*args, **kwargs)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint
                            | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setFixedSize(self.size, self.size)
        self.move(1, 1)
        self.hide()

    def move(self, x, y):
        super().move(x - self.size / 2, y - self.size/2)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        path = QPainterPath()
        radius = min(self.width(), self.height()) / 2
        path.addRoundedRect(QRectF(self.rect()), radius, radius)
        painter.setClipPath(path)

        painter.setPen(QPen(QColor(0, 174, 255), 3))
        hw = self.width() / 2
        hh = self.height() / 2
        painter.drawLines(QLineF(hw, 0, hw, self.height()),
                          QLineF(0, hh, self.width(), hh))
        painter.setPen(QPen(Qt.white, 3))
        painter.drawRoundedRect(self.rect(), radius, radius)


class ColorPicker(QPushButton):

    colorChanged = pyqtSignal(QColor)

    def __init__(self):
        super(ColorPicker, self).__init__()
        self.setIconSize(QSize(35, 35))
        self._setIcon()
        self._marker: QWidget = MarkerWindow()

        self._marker.show()
        self._marker.hide()
        self._isWatching = False

    def closeEvent(self, event):
        self._marker.close()
        super().closeEvent(event)

    def _setIcon(self, alt=False):
        self.setIcon(QIcon("icon/icon%s.png" % ("_alt" if alt else "")))

    def mousePressEvent(self, event):
        super(ColorPicker, self).mousePressEvent(event)
        self._isWatching = not self._isWatching

        if self._isWatching:
            self.setCursor(Qt.CrossCursor)
            self._setIcon(True)
            self._marker.show()
        else:
            self._setIcon()
            self._marker.hide()

    def mouseReleaseEvent(self, event):
        super(ColorPicker, self).mouseReleaseEvent(event)
        self.setCursor(Qt.ArrowCursor)

        if not self._isWatching:
            self._setIcon()

    def mouseMoveEvent(self, event):
        # getAverageColor(event, self.colorChanged.emit)
        pos = event.globalPos()
        self._marker.move(pos.x(), pos.y())


def getAverageColor(event, emit=None):
    pos = event.globalPos()
    image = QApplication.primaryScreen().grabWindow(
        int(QApplication.desktop().winId()),
        pos.x() - 6,
        pos.y() - 6, 13, 13).toImage()
    color = _getAverageColorFromImage(image)
    if emit and color.isValid():
        emit(color)


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
