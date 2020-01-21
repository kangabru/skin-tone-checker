from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QRect
from PyQt5.QtGui import QLinearGradient, QColor, QImage, QPainter, QPen, QBrush, QPainterPath
from PyQt5.QtWidgets import QSlider, QStyleOptionSlider, QStyle
from src.SkinToneHelper import HUE_TARGET
from typing import List, Tuple
from src.util import GetLinePath, SmoothPainter

INDICATOR_WIDTH, INDICATOR_HEIGHT = 4, 5

class ColorHueSlider(QSlider):
    def __init__(self, parent=None):
        super().__init__(Qt.Horizontal, parent)
        self._hue = 0
        self._imageRainbow = self._getGradientPixmap()
        self.setToolTip("Displays the hue of the picked colour. The ideal skin tone hue is marked by arrows.")

    def setHue(self, hue):
        self._hue = hue
        self.update()

    def updateColor(self, color: QColor):
        h = color.hsvHueF()
        self.setHue(h)

    def _getX(self):
        x = self._hue * self.width()
        return max(0, min(self.width(), x))

    def paintEvent(self, event):
        painter = SmoothPainter(self)

        raindow_rect = self.rect().adjusted(0, INDICATOR_HEIGHT, 0, -INDICATOR_HEIGHT)
        painter.drawImage(raindow_rect, self._imageRainbow)

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

    def _getGradientPixmap(self):
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor('#ff0000'))
        gradient.setColorAt(0.17, QColor('#ffff00'))
        gradient.setColorAt(0.33, QColor('#00ff00'))
        gradient.setColorAt(0.5, QColor('#00ffff'))
        gradient.setColorAt(0.67, QColor('#0000ff'))
        gradient.setColorAt(0.83, QColor('#ff00ff'))
        gradient.setColorAt(1, QColor('#ff0000'))

        image = QImage(self.width(), self.height(), QImage.Format_ARGB32)
        painter = SmoothPainter(image)
        painter.fillRect(self.rect(), gradient)
        return image
