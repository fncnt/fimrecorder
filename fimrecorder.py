#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSignal, QThread

from fimui import ui_fimwindow
import pyloncom
import pylonproc
import cv2
import numpy
def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = ui_fimwindow.Ui_fimWindow()
    ui.setupUi(window)

    camera = pyloncom.QCamera()
    #ui.actionRecord.toggled.connect(lambda: camera.exampleSlot("test"))
    #ui.actionRecord.toggled[bool].connect(camera.exampleSlot)
    camera.device_status[str].connect(ui.statusbar.showMessage)
    camera.grabInBackground()
    camera.is_grabbing.connect(lambda: ui.statusbar.showMessage("grabbing..."))

    #ui.actionRefresh.triggered.connect(camera.grabInBackground)
    #nullsignal = pyqtSignal() #don' want to  cancel single snapshots
    disposablecam = pylonproc.QCamSnapshot()
    dcthread = QThread()
    def saveSnapshot():
        disposablecam.moveToThread(dcthread)
        camera.frame_grabbed[numpy.ndarray].connect(disposablecam.processImg)
        dcthread.started.connect(lambda: disposablecam.startProcessing)
        dcthread.start()
        disposablecam.img_processed.connect(dcthread.quit)

    ui.actionSnapshot.triggered.connect(saveSnapshot)


    window.show()
    sys.exit(app.exec_())





if __name__ == "__main__":
    main()
