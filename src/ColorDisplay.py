from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QImage, QPen, QPainterPath, QBrush
from PyQt5.QtWidgets import QWidget
from typing import List, Tuple
from src.SkinToneHelper import PERFECT_TONES_CUBIC_POINTS, PERFECT_TONES_POINTS, DEBUG_PERFECT_TONES_POINTS, PROXIMITY_MAP
from src.util import GetLinePath, GetCubicPath, HueColorsToPixels


class ColorDisplay(QWidget):

    colorChanged = pyqtSignal(QColor)

    def __init__(self, *args, color=Qt.red, **kwargs):
        super(ColorDisplay, self).__init__(*args, **kwargs)
        self._color = QColor(color)
        self._image = None
        self._imagePointer = None
        self._pointerPos = None
        self._createPointer()
        self._initProximityMap()

    def _initProximityMap(self):
        image = PROXIMITY_MAP.mirrored(False, True).scaled(self.width(), self.height())
        self.proximityMap = image

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
        if DEBUG_PERFECT_TONES_POINTS:
            # Paint the internal skin tone line limits
            painter.setCompositionMode(QPainter.CompositionMode_Screen)
            painter.drawImage(self.rect(), self.proximityMap)

            # Paint the internal skin tone line
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver) # Reset to default
            painter.setPen(QPen(Qt.white, 2, Qt.DashLine, Qt.RoundCap))
            painter.drawPath(self._getLinePath(PERFECT_TONES_POINTS))

        # Paint the ideal skin tone line
        color = Qt.black if DEBUG_PERFECT_TONES_POINTS else Qt.yellow
        painter.setPen(QPen(color, 4, Qt.DashLine, Qt.RoundCap))
        painter.drawPath(self._getCubicPath(PERFECT_TONES_CUBIC_POINTS))

    def _getCubicPath(self, points: List[Tuple[int, int]]):
        """Returns a path to draw using the given color percentage points.
        Points should be a list of 4 tuples representing four (Saturation, Brightness) values as percentages.
        FYI the plot displays saturation left to right, and brightness top to bottom.
        """
        points_xy = HueColorsToPixels(points, self.width(), self.height())
        return GetCubicPath(points_xy)

    def _getLinePath(self, points: List[Tuple[int, int]]):
        points_xy = HueColorsToPixels(points, self.width(), self.height())
        return GetLinePath(points_xy)