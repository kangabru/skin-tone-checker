from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QColor

class ColorMessage(QLabel):

    def __init__(self):
        super(ColorMessage, self).__init__()
        self.setObjectName('picker_message')
        self.setText("Test")

    def updateMessage(self, color):
        color = QColor(color)
        self.setText(color.name())
