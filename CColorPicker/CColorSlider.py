from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QLinearGradient, QColor, QImage, QPainter, QPen
from PyQt5.QtWidgets import QSlider, QStyleOptionSlider, QStyle

class CColorSlider(QSlider):
    def __init__(self, parent=None):
        super(CColorSlider, self).__init__(Qt.Horizontal, parent)
        self.setObjectName('Custom_Color_Slider')
        self._x = 0
        self._isFirstShow = True
        self._imageRainbow = None

    def reset(self):
        self.setValue(0)

    def setX(self, x):
        x = max(0, min(self.width(), x))
        self._x = x
        self.update()

    def showEvent(self, event):
        super(CColorSlider, self).showEvent(event)
        if self._isFirstShow:
            self._isFirstShow = False
            self.gradientPixmap()

    def paintEvent(self, event):
        option = QStyleOptionSlider()
        self.initStyleOption(option)
        groove = self.style().subControlRect(QStyle.CC_Slider, option, QStyle.SC_SliderGroove, self)
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.drawImage(groove, self._imageRainbow)

        painter.setPen(QPen(Qt.black, 4))
        painter.drawLine(self._x, 0, self._x, self.height())

        painter.setPen(QPen(Qt.white, 1))
        hue_target = 20 # TODO Variable
        x_hue = hue_target / 360 * self.width()
        painter.drawLine(x_hue, 0, x_hue, self.height())


    def gradientPixmap(self):
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
        painter.fillRect(0, 0, self.width(), self.height(), gradient)
        painter.end()

    def updateColor(self, color: QColor):
        h = color.hsvHueF()
        posX = h * self.width()
        self.setX(posX)
