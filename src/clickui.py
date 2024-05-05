from trace import Trace
from pynput.mouse import Controller,Button
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from worker import Worker

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.click_count=True
        self.mouse=Controller()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 40, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.resize(200,200)
        # self.pushButton.clicked.connect(self.clicking)
        self.pushButton.clicked.connect(lambda:self.click(self.pushButton))
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setGeometry(QtCore.QRect(240, 65, 600, 120))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 285, 25))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())
        self.threadpool = QThreadPool()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Clicker"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.label.setText(_translate("MainWindow", "ready to use"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))

    def click(self,b):        
        if b==self.pushButton:
            worker = Worker(self.execute_this_fn) # Any other args, kwargs are passed to the run function
            worker.signals.result.connect(self.print_output)
            worker.signals.finished.connect(self.thread_complete)
            worker.signals.progress.connect(self.progress_fn)

            if self.click_count:
                    self.label.setText('IT IS CLICKING')
                    b.setText('PAUSE')
                    self.threadpool.start(worker)
                    self.click_count=not self.click_count
                    
            else:
                    self.label.setText('CLICKING IS PAUSED')
                    b.setText('START')
                    self.click_count=not self.click_count

   

    def execute_this_fn(self, progress_callback):
        while True:
            self.mouse.click(Button.left,1)
            print('clicking')
            time.sleep(5)
            if self.pushButton.isChecked():
                progress_callback.emit(100)
                break    

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def progress_fn(self, n):
        print("%d%% done" % n)







if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

