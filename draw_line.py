import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget)
from PyQt5.QtGui import QPainter, QBrush, QPen, QIcon, QPixmap, QColor
from PyQt5.QtCore import Qt

class MouseTracker(QWidget):
    distance_from_center = 0
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        self.setGeometry(20, 40, 500, 400)
        self.setWindowTitle('Mouse Tracker')
        self.label = QLabel(self)
        self.label.resize(500, 40)

        self.gambar = QLabel(self)
        pixmap = QPixmap('kompas.png')
        self.gambar.setPixmap(pixmap)
        self.gambar.resize(80,80)
        self.gambar.setScaledContents(1)
        self.gambar.move(110,160)

        self.painter = QPainter(self)
        self.painter.setPen(QPen(Qt.black,  5, Qt.SolidLine))
        self.painter.drawRect(0, 0, 300, 400)
        self.painter.setPen(QPen(Qt.red,  3, Qt.DotLine))
        self.painter.drawLine(0, 190, 300, 190)
        self.painter.drawLine(0, 210, 300, 210)
        self.painter.drawLine(140, 0, 140, 400)
        self.painter.drawLine(160, 0, 160, 400)
        
        self.show()
        self.pos = None

    def mouseMoveEvent(self, event):
        distance_from_center = round(((event.y() - 250)**2 + (event.x() - 500)**2)**0.5)
        self.label.setText('Coordinates: ( %d : %d )' % (event.x(), event.y()) + "Distance from center: " + str(distance_from_center))       
        self.pos = event.pos()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black,  5, Qt.SolidLine))
        painter.drawRect(0, 0, 300, 400)
        painter.setPen(QPen(Qt.red,  3, Qt.DotLine))
        painter.drawLine(0, 190, 300, 190)
        painter.drawLine(0, 210, 300, 210)
        painter.drawLine(140, 0, 140, 400)
        painter.drawLine(160, 0, 160, 400)
        #if self.pos:
        #    q = QPainter(self)
        #    q.drawLine(self.pos.x(), self.pos.y(), 250, 500)


app = QApplication(sys.argv)
ex = MouseTracker()
sys.exit(app.exec_())
