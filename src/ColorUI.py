from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget,\
    QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy,\
    QHBoxLayout, QApplication

from src.ColorCircle import ColorCircle
from src.ColorDisplay import ColorDisplay
from src.ColorHueSlider import ColorHueSlider
from src.ColorPicker import ColorPicker, getAverageColor
from src.styles import Stylesheet

class ColorUI(QDialog):

    selectedColor = QColor()
    colorChanged = pyqtSignal(QColor)

    def __init__(self, *args, **kwargs):
        super(ColorUI, self).__init__(*args, **kwargs)
        self.setObjectName('Custom_Color_Dialog')
        self.setStyleSheet(Stylesheet)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.initUi()
        self.initSignals()

    def initUi(self):
        vlayout = QVBoxLayout(self)
        colorView = QWidget(self)
        colorView.setObjectName('Custom_Color_View')
        vlayout.addWidget(colorView)

        vlayout = QVBoxLayout(colorView)
        vlayout.setContentsMargins(1, 1, 1, 1)

        self.colorDisplay = ColorDisplay()
        vlayout.addWidget(self.colorDisplay)

        color_tools = QWidget()
        vlayout.addWidget(color_tools)
        hlayout = QHBoxLayout(color_tools)

        self.colorPicker = ColorPicker()
        hlayout.addWidget(self.colorPicker)

        self.colorCircle = ColorCircle()
        hlayout.addWidget(self.colorCircle)

        self.hueIndicator = ColorHueSlider()
        hlayout.addWidget(self.hueIndicator)

    def initSignals(self):
        self.colorPicker.colorChanged.connect(self.colorDisplay.updateColor)
        self.colorPicker.colorChanged.connect(self.colorCircle.updateColor)
        self.colorPicker.colorChanged.connect(self.hueIndicator.updateColor)

        self.colorChanged.connect(self.colorDisplay.updateColor)
        self.colorChanged.connect(self.colorCircle.updateColor)
        self.colorChanged.connect(self.hueIndicator.updateColor)

    def mousePressEvent(self, event):
        self.setCursor(Qt.CrossCursor)

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.ArrowCursor)

    def mouseMoveEvent(self, event):
        getAverageColor(event, self.colorChanged.emit)
