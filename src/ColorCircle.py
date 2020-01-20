from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtWidgets import QWidget
from src.util import SmoothPainter

class ColorCircle(QWidget):
    def __init__(self, color=Qt.red):
        super(ColorCircle, self).__init__()
        self._color = QColor(color)
        self.setToolTip("Displays the current picked colour.")

    def updateColor(self, color):
        self._color = QColor(color)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        SmoothPainter(painter)

        diameter = min(self.width(), self.height()) - 8
        radius = diameter / 2
        path = QPainterPath()
        path.addRoundedRect(-radius, -radius, diameter, diameter, radius, radius)

        painter.translate(self.rect().center())
        painter.fillPath(path, self._color)
