import time
import sys
from PyQt6.QtCore import QObject, QThread, pyqtSignal, QTimer, QThreadPool

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication,QMainWindow, QLabel
from PyQt6.QtGui import * 


import defs
from worker import Worker

#app = QApplication(sys.argv)
Form, Window = uic.loadUiType("untitled.ui")  # из xml подгружаем Form, Window


 
class MainWindow(Window):
    def __init__(self,*args, **kwargs): 
        super(MainWindow, self).__init__(*args, **kwargs)
        # super().__init__()
        self.form = Form()
        self.form.setupUi(self)   

        self.form.ButtonPlay.clicked.connect(self.on_click) # обработчик события (нажатия кнопки)

        
        self.label = QLabel("press button", self) # !!! модификация нашего ui - добавили label
        # self.form.addWidget(self.l)
        
        self.show()

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())


        # self.timer = QTimer()
        # self.timer.setInterval(1000)
        # self.timer.timeout.connect(defs.on_timer)
        # self.timer.start()
  

    def progress_fn(self, n):
        defs.log_thread("")
        print(f"{n}% done")
        self.label.setText(f"{n}% done")  


    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")



    def on_click(self):
        print("clicked")
        # Pass the function to execute
        worker = Worker(defs.thread_fn) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)


def main():  
    app = QApplication(sys.argv) # создали QT app
    w = MainWindow()
    app.exec()  # и запускаем приложение (вечный цикл)

if __name__ == "__main__":
    main()