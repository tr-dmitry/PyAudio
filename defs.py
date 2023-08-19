import threading
import time

from PyQt6 import QtCore

 
def on_timer():
    print(".")

def thread_fn(progress_callback):
    for n in range(0, 5):
        time.sleep(1)
        progress_callback.emit(n*100//5) # вызываем функцию по событию (отсылаем сигнал)

    return "Done."

def log_thread(caller):
    print('%-25s: %s, %s,' % (caller, QtCore.QThread.currentThread().objectName(), int(QtCore.QThread.currentThreadId())))
    print('%-25s: %s, %s,' % (caller, threading.current_thread().name, threading.current_thread().ident))
