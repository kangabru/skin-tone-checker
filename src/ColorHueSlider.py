from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from PyQt5.QtGui import QLinearGradient, QColor, QImage, QPainter, QPen, QBrush, QPainterPath
from PyQt5.QtWidgets import QSlider, QStyleOptionSlider, QStyle
from src.SkinToneHelper import HUE_TARGET
from typing import List, Tuple
from src.util import GetLinePath

INDICATOR_WIDTH, INDICATOR_HEIGHT = 4, 5

class ColorHueSlider(QSlider):
    def __init__(self, parent=None):
        super(ColorHueSlider, self).__init__(Qt.Horizontal, parent)
        self._hue = 0
        self._isFirstShow = True
        self._imageRainbow = None

    def reset(self):
        self.setValue(0)

    def setHue(self, hue):
        self._hue = hue
        self.update()

    def _getX(self):
        x = self._hue * self.width()
        return max(0, min(self.width(), x))

    def showEvent(self, event):
        super(ColorHueSlider, self).showEvent(event)
        if self._isFirstShow:
            self._isFirstShow = False
            self.gradientPixmap()

    def paintEvent(self, event):
        option = QStyleOptionSlider()
        self.initStyleOption(option)
        groove = self.style().subControlRect(QStyle.CC_Slider, option, QStyle.SC_SliderGroove, self)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.setPen(Qt.NoPen)
        painter.drawImage(groove, self._imageRainbow)

        painter.setPen(QPen(Qt.black, 4))
        x_px = self._getX()
        painter.drawLine(x_px, 0, x_px, self.height())

        painter.setPen(QPen(Qt.black, 1))
        painter.setBrush(QBrush(Qt.black))

        x_hue, h = HUE_TARGET / 360 * self.width(), self.height()
        i_w, i_h = INDICATOR_WIDTH, INDICATOR_HEIGHT
        path_top = GetLinePath([(x_hue - i_w, 0), (x_hue + i_w, 0), (x_hue, i_h)])
        path_bot = GetLinePath([(x_hue - i_w, h), (x_hue + i_w, h), (x_hue, h - i_h)])
        painter.drawPath(path_top)
        painter.drawPath(path_bot)

    def gradientPixmap(self):
        h, o = self.height() - 2 * INDICATOR_HEIGHT, INDICATOR_HEIGHT
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor('#ff0000'))
        gradient.setColorAt(0.17, QColor('#ffff00'))
        gradient.setColorAt(0.33, QColor('#00ff00'))
        gradient.setColorAt(0.5, QColor('#00ffff'))
        gradient.setColorAt(0.67, QColor('#0000ff'))
        gradient.setColorAt(0.83, QColor('#ff00ff'))
        gradient.setColorAt(1, QColor('#ff0000'))
        self._imageRainbow = QImage(self.width(), self.height(), QImage.Format_ARGB32)

        painter = QPainter()
        painter.begin(self._imageRainbow)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.fillRect(0, o, self.width(), h, gradient)
        painter.end()

    def updateColor(self, color: QColor):
        h = color.hsvHueF()
        self.setHue(h)
