import sys
from PyQt5.QtGui import QPainter, QBrush, QPen, QIcon, QPixmap, QColor
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QMainWindow)


class MouseTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        self.setGeometry(20, 40, 500, 400)
        self.setWindowTitle('Mouse Tracker')
        self.label = QLabel(self)
        self.label.resize(200, 40)

        painter = QPainter(self)
        #painter.setPen(QPen(Qt.black,  5, Qt.SolidLine))
        #self.painter.drawRect(0, 0, 300, 400)
        #self.painter.setPen(QPen(Qt.red,  3, Qt.DotLine))
        painter.drawLine(0, 190, 300, 190)
        #self.painter.drawLine(0, 210, 300, 210)
        #self.painter.drawLine(140, 0, 140, 400)
        #self.painter.drawLine(160, 0, 160, 400)

       
        
        self.gambar = QLabel(self)
        pixmap = QPixmap('kompas.png')
        self.gambar.setPixmap(pixmap)
        self.gambar.resize(80,80)
        self.gambar.setScaledContents(1)
        self.gambar.move(110,160)


        self.show()

    """

    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.painter.setPen(QPen(Qt.black,  5, Qt.SolidLine))
        self.painter.drawRect(0, 0, 300, 400)
        self.painter.setPen(QPen(Qt.red,  3, Qt.DotLine))
        self.painter.drawLine(0, 190, 300, 190)
        self.painter.drawLine(0, 210, 300, 210)
        self.painter.drawLine(140, 0, 140, 400)
        self.painter.drawLine(160, 0, 160, 400)
    """
    def mouseMoveEvent(self, event):
        self.label.setText('Mouse coords: ( %d : %d )' % (event.x(), event.y()))
        self.update()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MouseTracker()
    sys.exit(app.exec_())
