from PyQt5.QtGui import QPainter, QBrush, QPen, QIcon, QPixmap, QColor
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import (QApplication, QCheckBox, QLabel, QWidget, QMainWindow)
import sys

#import time, datetime
import serial
import binascii

port = "/dev/ttyACM0"
rate = 57600

se = serial.Serial(port, rate)
from threading import Timer,Thread,Event

global a,b
b=0
a=0
global pwm, serv, dirct
pwm = 0
serv = 1550

dirct = 0
global textKirim
textKirim = 'A0B0C0D0E1550F\n'
            
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
        self.dataKirim.setText('A1B100C1D100E1500F\n')
        self.dataKirim.move(20,350)

        self.cb = QCheckBox("Open Serial",self)
        self.cb.stateChanged.connect(self.clickBox)
        self.cb.move(320,40)
        self.cb.resize(320,40)
        
        self.gambar = QLabel(self)
        pixmap = QPixmap('kompas.png')
        self.gambar.setPixmap(pixmap)
        self.gambar.resize(80,80)
        self.gambar.setScaledContents(1)
        self.gambar.move(110,160)

        
        self.show()

    def clickBox(self, state):
        if state == QtCore.Qt.Checked:
            global b
            b = 1
            try:
                #se = serial.Serial(port, rate)
                pass
            except:
                print ('port bermasalah!')
                
        else:
            global b
            b = 0

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
            global textKirim
            textKirim = 'A%dB%dC%dD%dE%dF\n' % (dirct,pwm,dirct,pwm,serv)
            self.dataKirim.setText(textKirim) 
            #self.dataKirim.setText('ok')
            #updateDataKirim(self)
        self.update()
        #update()

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
            
            self.dataKirim.setText('A%dB%dC%dD%dE%dF\n' % (dirct,pwm,dirct,pwm,serv)) 
        
    def mouseReleaseEvent(self, event):
        global a
        a=0
        global textKirim
        textKirim='A0B0C0D0E1550F\n'
        self.dataKirim.setText('A0B0C0D0E1550F\n')
        self.gambar.move(110,160)

        
def konversi(x,y):
    if y<190:
        global pwm, dirct
        pwm = (-255/200*y)+255
        dirct = 0
    elif y>210:
        global pwm, dirct, serv
        pwm = (-255/200*y) + (2*255)
        dirct = 1
    else:
        global pwm, dirct
        pwm = 0
        dirct = 0

    if x<140:
        global serv
        serv = (-8/3*x)+1950
    elif x>160:
        global serv
        serv = (-8/3*x)+1950
    else:
        global serv
        serv = 1550
#------------------------------------------------------      
class perpetualTimer():
   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

def printer():
    if b == 1:
        print (textKirim)
        try:
           se.write(str.encode(textKirim))
        except:
            print ('pengiriman data gagal')

t = perpetualTimer(0.4,printer)
t.start()
#------------------------------------------------------
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MouseTracker()
    sys.exit(app.exec_())


