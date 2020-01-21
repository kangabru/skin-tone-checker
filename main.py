import sys
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QApplication, QDesktopWidget

from src.ColorCircle import ColorCircle
from src.ColorDisplay import ColorDisplay
from src.ColorHueSlider import ColorHueSlider
from src.ColorPicker import ColorPicker, getAverageColor
from src.ColorMessage import ColorMessage, ColorStats
from src.styles import Stylesheet
from src.util import UpdateObjectName

class App(QDialog):

    colorChanged = pyqtSignal(QColor)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Skin Tone Checker")
        self.setGeometry(-1, -1, 250, -1) # left, top, width, height
        self.setWindowIcon(QIcon("icon/icon.png"))
        self.setToolTip("Right click to toggle whether to fix the app above other windows.")

        self._windowOnTop = False
        self.centerOnScreen()
        self.setStyleSheet(Stylesheet)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.initUi()
        self.initSignals()
        self.show()

    def initUi(self):
        vlayout = QVBoxLayout(self)
        content = QWidget(self)
        vlayout.addWidget(content)

        vlayout = QVBoxLayout(content)
        vlayout.setContentsMargins(0,0,0,0)

        self.colorDisplay = ColorDisplay()
        vlayout.addWidget(self.colorDisplay)

        color_tools = QWidget()
        vlayout.addWidget(color_tools)
        hlayout = QHBoxLayout(color_tools)

        self.colorPicker = ColorPicker(self._getWindowOnTop, self._setWindowOnTop)
        hlayout.addWidget(self.colorPicker)

        self.colorCircle = ColorCircle()
        hlayout.addWidget(self.colorCircle)

        self.hueIndicator = ColorHueSlider()
        hlayout.addWidget(self.hueIndicator)

        self.message = ColorMessage()
        vlayout.addWidget(self.message)

        self.stats = ColorStats()
        vlayout.addWidget(self.stats)

    def initSignals(self):
        self._connectColorUpdates(self.colorPicker.colorChanged.connect)
        self._connectColorUpdates(self.colorChanged.connect)

    def _connectColorUpdates(self, func):
        func(self.colorDisplay.updateColor)
        func(self.colorCircle.updateColor)
        func(self.hueIndicator.updateColor)
        func(self.message.updateMessage)
        func(self.stats.updateMessage)

    def mousePressEvent(self, event):
        self.colorPicker.stopWatching()
        
        if event.button() == Qt.RightButton:
            self._toggleWindowOnTop()
        else:
            self.setCursor(Qt.CrossCursor)

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.ArrowCursor)

    def mouseMoveEvent(self, event):
        getAverageColor(event, self.colorChanged.emit)

    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    def closeEvent(self, event):
        super().closeEvent(event)
        self.colorPicker.close()

    def _toggleWindowOnTop(self):
        self._setWindowOnTop(not self._windowOnTop)

    def _getWindowOnTop(self):
        return self._windowOnTop

    def _setWindowOnTop(self, windowOnTop):
        self._windowOnTop = windowOnTop
        self.setWindowFlag(Qt.WindowStaysOnTopHint, windowOnTop)
        self.show()
        UpdateObjectName(self.style(), self, "border" if windowOnTop else "")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())