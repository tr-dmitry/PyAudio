# import pyaudio
# import math
import time
from PyQt5.QtCore import QObject, QThread, pyqtSignal

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication

button_stop = None
button_play = None


def main():
    global button_stop
    global button_play
    Form, Window = uic.loadUiType("untitled.ui")
    app = QApplication([])
    window = Window()
    form = Form()
    form.setupUi(window)
    button_stop = form.ButtonStop
    button_play = form.ButtonPlay

    form.ButtonClose.clicked.connect(on_close)  # вызов функции
    button_play.clicked.connect(runLongTask)  # вызов функции
    button_stop.clicked.connect(on_close)  # вызов функции
    window.show()
    app.exec()  # вечный цикл и отслеживание событий


def on_close():
    print("close")


def runLongTask():
    """Long-running task in 5 steps."""
    # Step 2: Create a QThread object
    thread = QThread()
    # Step 3: Create a worker object
    worker = Worker()
    # Step 4: Move worker to the thread
    worker.moveToThread(thread)
    # Step 5: Connect signals and slots
    thread.started.connect(worker.run)
    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)
    thread.finished.connect(thread.deleteLater)
    worker.progress.connect(reportProgress)
    # Step 6: Start the thread
    thread.start()

    # Final resets
    button_stop.setEnabled(True)
    thread.finished.connect(
        lambda: button_stop.setEnabled(False)
    )
    button_play.setEnabled(False)
    thread.finished.connect(
        lambda: button_play.setEnabled(True)
    )
    thread.finished.connect(
        # lambda: stepLabel.setText("Long-Running Step: 0")
        lambda: print("Long-Running Step: 0")
    )
    print ("long r task st")

# Step 1: Create a worker class
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        """Long-running task."""
        for i in range(5):
            time.sleep(1)
            self.progress.emit(i + 1)
            #print("worker:", i)
        self.finished.emit()


def reportProgress(n):
    print(n)


"""
PyAudio = pyaudio.PyAudio
#See https://en.wikipedia.org/wiki/Bit_rate#Audio
BITRATE = 48000     #number of frames per second/frameset.

FREQUENCY = 500     #Hz, waves per second, 261.63=C4-note.
LENGTH = 1     #seconds to play sound

BITRATE = max(BITRATE, FREQUENCY+100)

NUMBEROFFRAMES = int(BITRATE * LENGTH)
RESTFRAMES = NUMBEROFFRAMES % BITRATE
WAVEDATA = ''

#generating wawes

for x in range(NUMBEROFFRAMES):
 WAVEDATA = WAVEDATA+chr(int(math.sin(x/((BITRATE/FREQUENCY)/math.pi))*127+128))

for x in range(RESTFRAMES):
 WAVEDATA = WAVEDATA+chr(128)

p = PyAudio()
stream = p.open(format = p.get_format_from_width(1),
                channels = 1,
                rate = BITRATE,
                output = True)

stream.write(WAVEDATA)
stream.stop_stream()
stream.close()
p.terminate()"""

if __name__ == "__main__":
    main()
