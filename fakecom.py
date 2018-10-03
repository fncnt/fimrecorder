import cv2
import numpy
import time
import os
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread


class QCamWorker(QObject):
    # Worker for QThreads
    # This Class grabs frames in the background
    # and pushes them to other threads responsible
    # for snapshots and recording
    # using pyqtSignal and pyqtSlot passing numpy images

    fakedevice = 'fakecamsource.avi'

    _cam = cv2.VideoCapture()
    device_stopped = pyqtSignal()
    frame_grabbed = pyqtSignal(numpy.ndarray)
    is_grabbing = pyqtSignal()
    device_status = pyqtSignal(str)
    device_name = pyqtSignal(str)
    # TODO overload signal to allow integer codes
    # 0: device found, using device
    # 1: no device found

    def __init__(self):
        super().__init__()
        self.connectToCam()

    def __del__(self):
        cv2.destroyWindow('Preview')
        super(QCamWorker, self).__del__()

    #check for compatible type in function
    #I'd like to avoid setters
    #but this way I don't have to  define a function for every Attribute
    @pyqtSlot(str, object)
    def setCamAttr(self, attribute: str, value):
        return 0

    def stop(self):
        #self.device_status.emit("Stopping frame-grabbing...")
        self._cam.release()

    @pyqtSlot()
    def connectToCam(self):
        try:
            self._cam.open(self.fakedevice)
            self.device_status.emit("Using fake device.")
            self.device_name.emit("fakecam")

        except BaseException as e:
            # Error handling.
            print("An exception occurred.")
            print(str(e))
            self.device_status.emit("No device found.")
            self.device_name.emit("no device")


    @pyqtSlot()
    def grabFrames(self):

        while self._cam.isOpened():
            self.is_grabbing.emit()
            # Access the image data
            retval, image = self._cam.read()
            img = image
            if retval:
                self.frame_grabbed.emit(img)
                time.sleep(0.024049)
            else:
                self.stop()
            # self.device_status.emit(str(type(img)))
            # Process finished with exit code 139 (interrupted by signal 11: SIGSEGV)
            #cv2.namedWindow('Preview', cv2.WINDOW_NORMAL)  # cv2.WINDOW_KEEPRATIO)
            #cv2.imshow('Preview', img)  # cv2.resize(img, dsize=(300, 300), interpolation=cv2.INTER_CUBIC))
            #self.device_status.emit("Grabbing..." + str(retval) + ", " + str(type(img)))
            #k = cv2.waitKey(25)
            #if k == 27:
            #    break

        self.device_status.emit("Stopped frame-grabbing.")
        self.device_stopped.emit()

# TODO: rename since QT5 provides a identically named class
class QCamera(QObject):
    #init camera on self.refresh()
    camThread = QThread()
    baslerace = QCamWorker()

    frame_grabbed = pyqtSignal(numpy.ndarray)
    is_grabbing = pyqtSignal()
    device_stop = pyqtSignal()
    device_status = pyqtSignal(str)
    device_name = pyqtSignal(str)

    #TODO overload signal to allow integer codes
    # 0: device found, using device
    # 1: no device found

    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def reset(self):
        self.stopGrabbing()
        self.baslerace.connectToCam()
        self.baslerace.grabFrames()

    # start thread with _grab
    @pyqtSlot()
    def grabInBackground(self):
        self.baslerace.moveToThread(self.camThread)
        # connect signals
        self.baslerace.device_name.connect(self.device_name)
        self.baslerace.device_status.connect(self.device_status)
        self.baslerace.frame_grabbed.connect(self.frame_grabbed)
        self.baslerace.is_grabbing.connect(self.is_grabbing)

        self.camThread.started.connect(self.baslerace.grabFrames)
        self.baslerace.connectToCam()
        self.camThread.start()

    def stopGrabbing(self):
        self.baslerace.stop()