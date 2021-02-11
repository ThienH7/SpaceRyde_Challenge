#!/usr/bin/env python

from PyQt5 import QtCore, QtGui, QtWidgets
from python_qt_binding import loadUi
import sys, random, math

class My_App(QtWidgets.QMainWindow):
    
    def __init__(self, position):
        super(My_App, self).__init__()
        self.setWindowTitle("Air Traffic")
        self.setGeometry(0, 0, 1000, 1000)
        self.center()

        # loadUi("./ATC.ui", self)

        # scene = QtWidgets.QGraphicsScene()
        # self.airSpace.setScene(scene)

        self.freq = 140.0/1000.0
        self.time = 0.0
        # self.posX = 50.0 * math.sin(self.freq*self.time)
        # self.posY = 50.0 * math.cos(self.freq*self.time)
        self.posX = position[0]
        self.posY = position[1]
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(100)

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def tick(self):
        self.time += 1.0
        # self.posX = 50.0 * math.sin(self.freq*self.time)
        # self.posY = 50.0 * math.cos(self.freq*self.time)

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()
        self.update()

    def drawPoints(self, qp):
        pen = QtGui.QPen(QtCore.Qt.red)
        pen.setWidth(10)
        qp.setPen(pen)
        qp.drawPoint(self.posX, self.posY)

    def updatePos(self, position):
        self.posX = position[0]
        self.posY = position[1]

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myApp = My_App([500, 500])
    myApp.show()

    sys.exit(app.exec_())