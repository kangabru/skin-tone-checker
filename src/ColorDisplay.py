from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QImage, QPen, QPainterPath, QBrush
from PyQt5.QtWidgets import QWidget


class ColorDisplay(QWidget):

    colorChanged = pyqtSignal(QColor)

    def __init__(self, *args, color=Qt.red, **kwargs):
        super(ColorDisplay, self).__init__(*args, **kwargs)
        self._color = QColor(color)
        self._image = None
        self._imagePointer = None       # 小圆环
        self._pointerPos = None         # 小圆环位置
        self._createPointer()

    def reset(self):
        self.blockSignals(True)
        self._color = QColor(Qt.red)
        self._pointerPos = self.rect().topRight()
        self.update()
        self.blockSignals(False)

    def _createPointer(self):
        self._imagePointer = QImage(12, 12, QImage.Format_ARGB32)
        self._imagePointer.fill(Qt.transparent)
        painter = QPainter()
        painter.begin(self._imagePointer)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.setPen(QPen(Qt.white, 2))
        painter.setBrush(Qt.NoBrush)
        path = QPainterPath()
        path.addRoundedRect(0, 0, 12, 12, 6.0, 6.0)
        painter.setClipPath(path)
        painter.drawRoundedRect(0, 0, 12, 12, 6.0, 6.0)
        painter.end()

    def paintEvent(self, event):
        super(ColorDisplay, self).paintEvent(event)
        if self._image:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
            painter.drawImage(self.rect(), self._image)
            painter.setPen(QColor(240, 240, 240))
            painter.drawRect(self.rect())
            if self._pointerPos:
                painter.setPen(Qt.NoPen)
                painter.drawImage(self._pointerPos - QPoint(6, 6), self._imagePointer)

    def resizeEvent(self, event):
        super(ColorDisplay, self).resizeEvent(event)
        self.updateColor(self._color)

    def updateColor(self, color):
        """Sets the top right color of the panel."""
        color = QColor(color)
        color.setAlpha(255)

        self._color = color
        self._image = QImage(self.size(), QImage.Format_ARGB32)

        painter = QPainter()
        painter.begin(self._image)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        # Render top right corner
        # Choose brightest, most saturated color for the given hue. Undefined hues (greys) should default to red hue.
        h = max(0, color.hsvHue())
        color_full = QColor.fromHsv(h, 255, 255)
        painter.fillRect(self.rect(), color_full)

        # Create vertical shading
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, Qt.white)
        gradient.setColorAt(1, QColor.fromHslF(0.055, 0.42, 0.65, 0))
        painter.fillRect(self.rect(), gradient)

        # Create horizontal shading
        gradient = QLinearGradient(0, self.height(), 0, 0)
        gradient.setColorAt(1, QColor.fromHslF(0.055, 0.42, 0.65, 0))
        gradient.setColorAt(0, Qt.black)
        painter.fillRect(self.rect(), gradient)

        self._createSkinToneIndicator(painter)
        painter.end()

        w, h = self.width(), self.height()
        _, s, v, _ = color.getHsvF()
        x, y = s * w, (1 - v) * h
        self._pointerPos = QPoint(x, y)

        self.update()


    def _createSkinToneIndicator(self, painter: QPainter):
        w, h = self.width(), self.height()

        # (Saturation, Brightness) as percentage
        points = [
            (20, 58),
            (20, 90),
            (33, 85),
            (37, 75),
            (39, 51),
            (52, 32),
            (71, 20),
        ]

        points_xy = [(p[0] / 100 * w, h - (p[1] / 100 * h)) for p in points]
        painter.setPen(QPen(Qt.white, 2, Qt.DashDotLine))
        path = QPainterPath()

        _x, _y = None, None
        for x, y in points_xy:
            if _x is not None:
                path.lineTo(x, y)
            path.moveTo(x, y)
            _x, _y = x, y

        painter.drawPath(path)

        points = [
            (20, 90),
            (60, 85),
            (20, 40),
            (71, 20),
        ]

        points_xy = [(p[0] / 100 * w, h - (p[1] / 100 * h)) for p in points]
        painter.setPen(QPen(Qt.yellow, 2, Qt.SolidLine))
        path = QPainterPath()

        x0, y0 = points_xy[0]
        x1, y1 = points_xy[1]
        x2, y2 = points_xy[2]
        x3, y3 = points_xy[3]
        path.moveTo(x0, y0)
        path.cubicTo(x1, y1, x2, y2, x3, y3)
        painter.drawPath(path)
