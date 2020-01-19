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


class ColorPickerUI(QDialog):

    selectedColor = QColor()
    colorChanged = pyqtSignal(QColor)

    def __init__(self, *args, **kwargs):
        super(ColorPickerUI, self).__init__(*args, **kwargs)
        self.setObjectName('Custom_Color_Dialog')
        self.setStyleSheet(Stylesheet)
        self.mPos = None
        self.initUi()
        self.initSignals()

    def initUi(self):
        layout = QVBoxLayout(self)
        self.colorView = QWidget(self)
        self.colorView.setObjectName('Custom_Color_View')
        layout.addWidget(self.colorView)


        layout = QVBoxLayout(self.colorView)
        layout.setContentsMargins(1, 1, 1, 1)


        self.colorPanel = ColorDisplay(self.colorView)
        layout.addWidget(self.colorPanel)

        self.controlWidget = QWidget(self.colorView)
        layout.addWidget(self.controlWidget)
        clayout = QHBoxLayout(self.controlWidget)

        self.colorStraw = ColorPicker(self.colorView)
        clayout.addWidget(self.colorStraw)

        self.colorControl = ColorCircle(self.colorView)
        clayout.addWidget(self.colorControl)

        self.sliderWidget = QWidget(self.colorView)
        clayout.addWidget(self.sliderWidget)
        slayout = QVBoxLayout(self.sliderWidget)
        slayout.setContentsMargins(0, 0, 0, 0)

        self.rainbowSlider = ColorHueSlider(self.colorView)
        slayout.addWidget(self.rainbowSlider)

    def initSignals(self):
        self.colorStraw.colorChanged.connect(self.colorPanel.updateColor)
        self.colorStraw.colorChanged.connect(self.colorControl.updateColor)
        self.colorStraw.colorChanged.connect(self.rainbowSlider.updateColor)

        self.colorChanged.connect(self.colorPanel.updateColor)
        self.colorChanged.connect(self.colorControl.updateColor)
        self.colorChanged.connect(self.rainbowSlider.updateColor)

    def setColor(self, color, alpha):
        color = QColor(color)
        color.setAlpha(alpha)
        ColorPickerUI.selectedColor = color

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mPos = event.pos()
        event.accept()

    def mouseReleaseEvent(self, event):
        self.mPos = None
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.mPos:
            if not self.colorPanel.geometry().contains(self.mPos):
                self.move(self.mapToGlobal(event.pos() - self.mPos))
        event.accept()

    def mousePressEvent(self, event):
        self.setCursor(Qt.CrossCursor)

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.ArrowCursor)

    def mouseMoveEvent(self, event):
        getAverageColor(event, self.colorChanged.emit)

    @classmethod
    def getColor(cls, parent=None):
        if not hasattr(cls, '_colorPicker'):
            cls._colorPicker = ColorPickerUI(parent)
        ret = cls._colorPicker.exec_()
        if ret != QDialog.Accepted:
            return ret, QColor()
        return ret, ColorPickerUI.selectedColor
