from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QColor
from src.SkinToneHelper import getSkinToneMessage, ErrorLevel

class ColorStats(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self._setMessage("#ff0000", 0, 100, 100)

    def updateMessage(self, color):
        color = QColor(color)
        h, s, v, _ = color.getHsv()
        self._setMessage(color.name(), h, s/2.55, v/2.55)

    def _setMessage(self, hex: str, hue: float, sat: float, bright: float):
        message = "%s H:%.0f S:%.0f%s B:%.0f%s" % (hex, hue, sat, "%", bright, "%")
        self.setText(message)


class ColorMessage(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setText("Click and drag anywhere to select colors.")

    def updateMessage(self, color):
        color = QColor(color)
        level, message = getSkinToneMessage(color)
        color = "blue" if level == ErrorLevel.good else "green" if level == ErrorLevel.ok else "black"
        self.setStyleSheet("color: %s;" % color)
        self.setText(message)
