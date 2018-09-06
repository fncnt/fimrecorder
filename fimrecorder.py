#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QPixmap

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
    camera.device_status[str].connect(print)

    if camera.baslerace._cam.IsOpen():
        camera.grabInBackground()
    #camera.is_grabbing.connect(lambda: ui.statusbar.showMessage("grabbing..."))

    ui.actionRefresh.triggered.connect(camera.reset)
    #ui.ExpTimeSpinBox.valueChanged[int].connect(camera.setExposureTime)
    #Replace lambda by functools.partial?
    ui.ExpTimeSpinBox.valueChanged[int].connect(
        lambda val: camera.baslerace.setCamAttr("ExposureTime", 1000 * val))

    disposablecam = pylonproc.QCamSnapshot()
    dcthread = QThread()
    def saveSnapshot():
        disposablecam.moveToThread(dcthread)

        # Is that really necessary? Shouldn't and shouldn't work!
        #camera.frame_grabbed[numpy.ndarray].connect(disposablecam.processImg)
        disposablecam.status[str].connect(print)
        dcthread.started.connect(lambda: disposablecam.startProcessing(camera.frame_grabbed))
        dcthread.start()
        disposablecam.img_processed.connect(dcthread.quit)

    ui.actionSnapshot.triggered.connect(saveSnapshot)

    recordingcam = pylonproc.QCamRecorder()
    recordingcam.status.connect(print)
    recthread = QThread()
    #recordingcam.img_processed.connect(recthread.wait)
    recordingcam.moveToThread(recthread)

    def recordVideo(toggled=bool):
        if toggled:
            #recordingcam.moveToThread(recthread)
            #recthread.started.connect(lambda: recordingcam.startProcessing(camera.frame_grabbed))
            recthread.start()
            recordingcam.startProcessing(camera.frame_grabbed)
        else:
            recordingcam.cancelProcessing()
            # Does terminate without blocking main thread. However, restarting doesn't really work
            # Also it's actually not recommended
            recthread.terminate()
            #recthread.quit()
            #recthread.wait(100)
    #recthread.finished.connect(recordingcam.deleteLater)

    ui.actionRecord.toggled[bool].connect(recordVideo)

    #previewthread = QThread()
    #ui.camView.moveToThread(previewthread)
    #previewthread.start()

    #previewcam = pylonproc.QCamQPixmap()
    #pcthread = QThread()
    #previewcam.moveToThread(pcthread)
    #previewcam.img_processed.connect(ui.camView.setPixmap)
    #camera.frame_grabbed[numpy.ndarray].connect(previewcam.processImg)
    #pcthread.started.connect(lambda: previewcam.startProcessing(camera.frame_grabbed))
    #pcthread.start()
    #ui.camView.setScaledContents(True)

    #app.aboutToQuit.connect(pcthread.quit)


    window.show()
    sys.exit(app.exec_())





if __name__ == "__main__":
    main()
