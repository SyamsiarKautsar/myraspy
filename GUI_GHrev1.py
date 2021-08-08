from PyQt5.QtGui import QPainter, QBrush, QPen, QIcon, QPixmap, QColor
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QMainWindow)
import sys

global a
a=0
global pwm, serv, dirct
pwm = 0
serv = 1550

dirct = 0

            
class MouseTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.painter = QPainter(self)
        self.painter.setPen(QPen(Qt.black,  5, Qt.SolidLine))
        self.painter.drawRect(0, 0, 300, 400)
        self.setMouseTracking(True)

    def initUI(self):
        self.setGeometry(20, 40, 500, 400)
        self.setWindowTitle('Green House GUI')
        self.label = QLabel(self)
        self.label.resize(200, 40)

        self.dataKirim = QLabel(self)
        self.dataKirim.resize(200, 40)
        self.dataKirim.setText('A1B100C1D100E1500F')
        self.dataKirim.move(20,350)
            
        self.gambar = QLabel(self)
        pixmap = QPixmap('kompas.png')
        self.gambar.setPixmap(pixmap)
        self.gambar.resize(80,80)
        self.gambar.setScaledContents(1)
        self.gambar.move(110,160)
        self.show()

    def paintEvent(self,event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black,  5, Qt.SolidLine))
        painter.drawRect(0, 0, 300, 400)
        painter.setPen(QPen(Qt.red,  3, Qt.DotLine))
        painter.drawLine(0, 190, 300, 190)
        painter.drawLine(0, 210, 300, 210)
        painter.drawLine(140, 0, 140, 400)
        painter.drawLine(160, 0, 160, 400)
    
    def mouseMoveEvent(self, event):
        self.label.setText('Mouse coords: ( %d : %d )' % (event.x(), event.y()))
        x = event.x()
        y = event.y()

        if x>300:
            x=300
        if x<0:
            x=0
        if y<0:
            y=0
        if y>400:
            y=400
            
        if a == 1:
            self.gambar.move(x-40,y-40)
            konversi(x,y)
            self.dataKirim.setText('A%dB%dC%dD%dE%dF' % (dirct,pwm,dirct,pwm,serv)) 
            #self.dataKirim.setText('ok')
            #updateDataKirim(self)
        self.update()

    def mousePressEvent(self, event):
        global a
        a=1

        x = event.x()
        y = event.y()
        
        if x>300:
            x=300
        if x<0:
            x=0
        if y<0:
            y=0
        if y>400:
            y=400
            
        if a == 1:
            self.gambar.move(x-40,y-40)
            konversi(x,y)
            self.dataKirim.setText('A%dB%dC%dD%dE%dF' % (dirct,pwm,dirct,pwm,serv)) 
        
    def mouseReleaseEvent(self, event):
        global a
        a=0
        self.dataKirim.setText('A0B0C0D0E1550F')
        self.gambar.move(110,160)

        
def konversi(x,y):
    if y<190:
        global pwm, dirct
        pwm = (-255/200*y)+255
        dirct = 0
    elif y>210:
        global pwm, dirct
        pwm = (-255/200*y) + (2*255)
        dirct = 1
    else:
        global pwm, dirct
        pwm = 0
        dirct = 0   
        
        
    #def updateDataKirim(self):
        #self.dataKirim.setText('ok')
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MouseTracker()
    sys.exit(app.exec_())
