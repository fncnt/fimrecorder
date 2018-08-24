import cv2
import numpy
import time
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread

class QCamProcessor(QObject):

    img_processed = pyqtSignal(object)
    is_running = pyqtSignal()
    is_processing = pyqtSignal(numpy.ndarray)

    def __init__(self):
        super().__init__()
        self._cancel = False

    #Only this method should be overridden
    @pyqtSlot(numpy.ndarray)
    def processImg(self, img=numpy.ndarray):
        return 0

    def startProcessing(self, img_received=pyqtSignal(numpy.ndarray)):
        #Handle QThread related stuff (i.e. signals and stuff here)
        #This runs in MainThread so don't put loops here.
        #processImg runs in separate thread.
        self.is_processing = img_received
        self.is_processing[numpy.ndarray].connect(self.processImg)

        #while not self._cancel:
        #    self.is_running.emit()
            #self.processImg(img)
        #self.finishProcessing()

    #when cancel signal is received
    def cancelProcessing(self):
        self.is_processing[numpy.ndarray].disconnect()
        self._cancel = True

    #clean up processing, i.e. save file etc.
    def finishProcessing(self):
        self.img_processed.emit()
        return 0


#class QCamRecorder(QCamProcessor):

class QCamQPixmap(QCamProcessor):

    def processImg(self, img=numpy.ndarray):
        aölsdk


class QCamSnapshot(QCamProcessor):

    def processImg(self, img=numpy.ndarray):
        #currenttime = time.strftime('%d.%m.%Y_%H:%M:%S', time.localtime())
        #cv2.imwrite(currenttime, img)
        cv2.imwrite('FIMsnapshot.png', img)
        self.cancelProcessing() #we just want to save one frame, so when we receive one, we immediately stop.


