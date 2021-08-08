from PyQt5.QtGui import QPainter, QBrush, QPen, QIcon, QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
#from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QMainWindow)
import sys

class Window(QMainWindow):
    def __init__(self):                       
        super().__init__()
        self.title = "GUI Robot Green House"
        self.top= 20
        self.left= 40
        self.width = 500
        self.height = 500
        
        self.InitWindow()
        self.setMouseTracking(True)
       
    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.gambar = QLabel(self)
        pixmap = QPixmap('kompas.png')
        self.gambar.setPixmap(pixmap)
        self.gambar.resize(80,80)
        self.gambar.setScaledContents(1)
        self.gambar.move(110,160)

        labelMouse = QLabel(self)
        labelMouse.resize(200, 40)
        labelMouse.setText('Mouse coords:0 0')


        self.show()

    def mouseMoveEvent(self, event):
        self.labelMouse.setText('wow')
        #labelMouse.setText('Mouse coords: 1')#( %d : %d )' % (event.x(), event.y()))
        pass
        
    def paintEvent(self):
        self.painter = QPainter(self)
        self.painter.setPen(QPen(Qt.black,  5, Qt.SolidLine))
        self.painter.drawRect(0, 0, 300, 400)
        self.painter.setPen(QPen(Qt.red,  3, Qt.DotLine))
        self.painter.drawLine(0, 190, 300, 190)
        self.painter.drawLine(0, 210, 300, 210)
        self.painter.drawLine(140, 0, 140, 400)
        self.painter.drawLine(160, 0, 160, 400)

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
