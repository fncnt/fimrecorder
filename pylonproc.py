import cv2
import numpy
import time
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread

class QCamProcessor(QObject):

    img_processed = pyqtSignal(object)
    is_processing = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._cancel = False
        #cancel.connect(self.cancelProcessing)

    @pyqtSlot(numpy.ndarray)
    def processImg(self, img=numpy.ndarray):
        return 0

    def startProcessing(self, img_received=pyqtSignal(numpy.ndarray)):
        #Handle QThread related stuff (i.e. signals and stuff here)
        img_received[numpy.ndarray].connect(self.processImg)

        while not self._cancel:
            self.is_processing.emit()
            #self.processImg(img)
        self.finishProcessing()

    #when cancel signal is received
    def cancelProcessing(self):
        self._cancel = True

    #clean up processing, i.e. save file etc.
    def finishProcessing(self):
        self.img_processed.emit()
        return 0


#class QCamRecorder(QCamProcessor):

#class QCamQPixmap(QCamProcessor):

class QCamSnapshot(QCamProcessor):

    def processImg(self, img=numpy.ndarray):
        cv2.imwrite('test.png', img)
        self.cancelProcessing() #we just want to save one frame, so when we receive one, we immediately stop.


