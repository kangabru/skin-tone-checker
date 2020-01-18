from PyQt5.QtCore import QByteArray, Qt, QRectF, QLineF, pyqtSignal
from PyQt5.QtGui import QFontDatabase, QFont, QPainter,\
    QPainterPath, QColor, QPen
from PyQt5.QtWidgets import QPushButton, QApplication, QWidget

FONT = b'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'


class ScaleWindow(QWidget):


    def __init__(self, *args, **kwargs):
        super(ScaleWindow, self).__init__(*args, **kwargs)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint |
                            Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.resize(1, 1)
        self.move(1, 1)
        self._image = None

    def updateImage(self, pos, image):
        self._image = image
        self.resize(image.size())
        self.move(pos.x() + 10, pos.y() + 10)
        self.show()
        self.update()

    def paintEvent(self, event):
        super(ScaleWindow, self).paintEvent(event)
        if self._image:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing, True)
            path = QPainterPath()
            radius = min(self.width(), self.height()) / 2
            path.addRoundedRect(QRectF(self.rect()), radius, radius)
            painter.setClipPath(path)

            painter.drawImage(self.rect(), self._image)

            painter.setPen(QPen(QColor(0, 174, 255), 3))
            hw = self.width() / 2
            hh = self.height() / 2
            painter.drawLines(
                QLineF(hw, 0, hw, self.height()),
                QLineF(0, hh, self.width(), hh)
            )

            painter.setPen(QPen(Qt.white, 3))
            painter.drawRoundedRect(self.rect(), radius, radius)


class CColorStraw(QPushButton):

    colorChanged = pyqtSignal(QColor)

    def __init__(self, parent):
        super(CColorStraw, self).__init__(parent)
        QFontDatabase.addApplicationFontFromData(QByteArray.fromBase64(FONT))
        font = self.font() or QFont()
        font.setFamily('iconfont')
        self.setFont(font)
        self.setText('')
        self.setToolTip('吸取屏幕颜色')
        self._scaleWindow = ScaleWindow()

        self._scaleWindow.show()
        self._scaleWindow.hide()

    def closeEvent(self, event):
        self._scaleWindow.close()
        super(CColorStraw, self).closeEvent(event)

    def mousePressEvent(self, event):
        super(CColorStraw, self).mousePressEvent(event)

        self.setCursor(Qt.CrossCursor)

    def mouseReleaseEvent(self, event):
        super(CColorStraw, self).mouseReleaseEvent(event)

        self.setCursor(Qt.ArrowCursor)
        self._scaleWindow.hide()

    def mouseMoveEvent(self, event):
        super(CColorStraw, self).mouseMoveEvent(event)

        pos = event.globalPos()

        image = QApplication.primaryScreen().grabWindow(
            int(QApplication.desktop().winId()),
            pos.x() - 6, pos.y() - 6, 13, 13).toImage()
        color = image.pixelColor(6, 6)
        if color.isValid():
            self.colorChanged.emit(color)
        self._scaleWindow.updateImage(pos, image.scaled(130, 130))


