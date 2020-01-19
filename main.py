import sys
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QApplication, QDesktopWidget

from src.ColorCircle import ColorCircle
from src.ColorDisplay import ColorDisplay
from src.ColorHueSlider import ColorHueSlider
from src.ColorPicker import ColorPicker, getAverageColor
from src.styles import Stylesheet

class App(QDialog):

    colorChanged = pyqtSignal(QColor)

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.setWindowTitle("Skin Color Picker")
        self.setGeometry(-1, -1, 250, -1) # left, top, width, height

        self.centerOnScreen()
        self.setObjectName('Custom_Color_Dialog')
        self.setStyleSheet(Stylesheet)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.initUi()
        self.initSignals()
        self.show()

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

    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())