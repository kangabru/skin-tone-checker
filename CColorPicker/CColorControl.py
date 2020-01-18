from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtWidgets import QWidget

class CColorControl(QWidget):

    colorChanged = pyqtSignal(QColor)

    def __init__(self, *args, color=Qt.red, **kwargs):
        super(CColorControl, self).__init__(*args, **kwargs)
        self._alpha = 255
        self._color = QColor(color)
        self.colorChanged.emit(self._color)

    def updateColor(self, color, alpha=255):
        self._color = QColor(color)
        self.colorChanged.emit(self._color)
        self._color.setAlpha(alpha)
        self.update()

    def reset(self):
        self.updateColor(Qt.red)

    def paintEvent(self, event):
        super(CColorControl, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.setPen(Qt.NoPen)


        painter.translate(self.rect().center())


        painter.save()

        diameter = min(self.width(), self.height()) - 8
        radius = diameter / 2
        path = QPainterPath()
        path.addRoundedRect(-radius, -radius, diameter,
                            diameter, radius, radius)
        painter.setClipPath(path)

        pixSize = 5
        for x in range(int(self.width() / pixSize)):
            for y in range(int(self.height() / pixSize)):
                _x, _y = x * pixSize, y * pixSize
                painter.fillRect(_x - radius, _y - radius, pixSize, pixSize,
                                 Qt.white if x % 2 != y % 2 else Qt.darkGray)
        painter.restore()


        diameter = min(self.width(), self.height()) - 4
        radius = diameter / 2
        path = QPainterPath()
        path.addRoundedRect(-radius, -radius, diameter,
                            diameter, radius, radius)
        painter.setClipPath(path)

        painter.setBrush(self._color)
        painter.drawRoundedRect(-radius, -radius,
                                diameter, diameter, radius, radius)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = CColorControl()
    w.resize(200, 200)
    w.show()
    sys.exit(app.exec_())
