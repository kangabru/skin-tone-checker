#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年4月19日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: CColorPicker.CColorPicker
@description:
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget,\
    QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy,\
    QHBoxLayout, QPushButton

from CColorPicker.CColorControl import CColorControl
from CColorPicker.CColorInfos import CColorInfos
from CColorPicker.CColorPalettes import CColorPalettes
from CColorPicker.CColorPanel import CColorPanel
from CColorPicker.CColorSlider import CColorSlider
from CColorPicker.CColorStraw import CColorStraw


__Author__ = "Irony"
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0

Stylesheet = """
QLineEdit, QLabel, QTabWidget {
    font-family: -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Oxygen,Ubuntu,Cantarell,Fira Sans,Droid Sans,Helvetica Neue,sans-serif;
}
#Custom_Color_View {
    background: white;
    border-radius: 3px;
}
CColorPalettes {
    min-width: 322px;
    max-width: 322px;
    max-height: 120px;
}
CColorPanel {
    min-height: 160px;
    max-height: 160px;
}
CColorControl {
    min-width: 50px;
    max-width: 50px;
    min-height: 50px;
    max-height: 50px;
}

#editHex {
    min-width: 75px;
}

#splitLine {
    min-height: 1px;
    max-height: 1px;
    background: #e2e2e2;
}

QLineEdit, QSpinBox {
    border: 1px solid #cbcbcb;
    border-radius: 2px;
    background: white;
    min-width: 31px;
    min-height: 21px;
}
QLineEdit:focus, QSpinBox:focus {
    border-color: rgb(139, 173, 228);
}
QLabel {
    color: #a9a9a9;
}
QPushButton {
    border: 1px solid #cbcbcb;
    border-radius: 2px;
    min-width: 21px;
    max-width: 21px;
    min-height: 21px;
    max-height: 21px;
    font-size: 14px;
    background: white;
}
QPushButton:hover {
    border-color: rgb(139, 173, 228);
}
QPushButton:pressed {
    border-color: #cbcbcb;
}

CColorStraw {
    border: none;
    font-size: 18px;
    border-radius: 0px;
}
QPushButton:hover {
    color: rgb(139, 173, 228);
}
QPushButton:pressed {
    color: #cbcbcb;
}

#confirmButton, #cancelButton {
    min-width: 70px;
    min-height: 30px;
}
#cancelButton:hover {
    border-color: rgb(255, 133, 0);
}

QTabWidget::pane {
    border: none;
}
QTabBar::tab {
    padding: 3px 6px;
    color: rgb(100, 100, 100);
    background: transparent;
}
QTabBar::tab:hover {
    color: black;
}
QTabBar::tab:selected {
    color: rgb(139, 173, 228);
    border-bottom: 2px solid rgb(139, 173, 228);
}

QTabBar::tab:!selected {
    border-bottom: 2px solid transparent;
}

QScrollBar:vertical {
    max-width: 10px;
    border: none;
    margin: 0px 0px 0px 0px;
}

QScrollBar::handle:vertical {
    background: rgb(220, 220, 220);
    border: 1px solid rgb(207, 207, 207);
    border-radius: 5px;
}
"""


class CColorPicker(QDialog):

    selectedColor = QColor()

    def __init__(self, *args, **kwargs):
        super(CColorPicker, self).__init__(*args, **kwargs)
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

        # 内部布局
        layout = QVBoxLayout(self.colorView)
        layout.setContentsMargins(1, 1, 1, 1)

        # 面板
        self.colorPanel = CColorPanel(self.colorView)
        layout.addWidget(self.colorPanel)

        self.controlWidget = QWidget(self.colorView)
        layout.addWidget(self.controlWidget)
        clayout = QHBoxLayout(self.controlWidget)

        # 取色器
        self.colorStraw = CColorStraw(self.colorView)
        clayout.addWidget(self.colorStraw)
        # 小圆
        self.colorControl = CColorControl(self.colorView)
        clayout.addWidget(self.colorControl)

        self.sliderWidget = QWidget(self.colorView)
        clayout.addWidget(self.sliderWidget)
        slayout = QVBoxLayout(self.sliderWidget)
        slayout.setContentsMargins(0, 0, 0, 0)
        # 滑动条
        self.rainbowSlider = CColorSlider(self.colorView)
        slayout.addWidget(self.rainbowSlider)

    def initSignals(self):
        self.colorPanel.colorChanged.connect(self.colorControl.updateColor)
        self.colorStraw.colorChanged.connect(self.colorPanel.createImage)
        self.colorStraw.colorChanged.connect(self.colorControl.updateColor)
        self.colorStraw.colorChanged.connect(self.rainbowSlider.updateColor)

    def setColor(self, color, alpha):
        color = QColor(color)
        color.setAlpha(alpha)
        CColorPicker.selectedColor = color

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.mPos = event.pos()
        event.accept()

    def mouseReleaseEvent(self, event):
        '''鼠标弹起事件'''
        self.mPos = None
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.mPos:
            if not self.colorPanel.geometry().contains(self.mPos):
                self.move(self.mapToGlobal(event.pos() - self.mPos))
        event.accept()

    @classmethod
    def getColor(cls, parent=None):
        """获取选择的颜色
        :param cls:
        :param parent:
        """
        if not hasattr(cls, '_colorPicker'):
            cls._colorPicker = CColorPicker(parent)
        ret = cls._colorPicker.exec_()
        if ret != QDialog.Accepted:
            return ret, QColor()
        return ret, CColorPicker.selectedColor


def test():
    import sys
    import cgitb
    sys.excepthook = cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication, QLabel
    app = QApplication(sys.argv)

    def getColor():
        ret, color = CColorPicker.getColor()
        if ret == QDialog.Accepted:
            r, g, b, a = color.red(), color.green(), color.blue(), color.alpha()
            label.setText('color: rgba(%d, %d, %d, %d)' % (r, g, b, a))
            label.setStyleSheet(
                'background: rgba(%d, %d, %d, %d);' % (r, g, b, a))

    window = QWidget()
    window.resize(200, 200)
    layout = QVBoxLayout(window)
    label = QLabel('', window, alignment=Qt.AlignCenter)
    button = QPushButton('点击选择颜色', window, clicked=getColor)
    layout.addWidget(label)
    layout.addWidget(button)
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    test()
