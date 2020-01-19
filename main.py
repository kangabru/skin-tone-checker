import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QColorDialog, QDesktopWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QColor

from src.ColorPickerUI import ColorPickerUI

class App(ColorPickerUI):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Skin Color Picker")
        self.setGeometry(-1, -1, 250, -1) # left, top, width, height
        self.centerOnScreen()
        self.show()

    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    @pyqtSlot()
    def on_click(self):
        ret, color = ColorPickerUI.getColor()
        if ret == ColorPickerUI.Accepted:
            print(color.name())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())