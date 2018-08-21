import cv2
import numpy
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread

class QCamProcessor(QObject):

    img_processed = pyqtSignal(object)

    def processImg(self, img=numpy.ndarray):
        #Do the work here

    def startProcessing(self, img=numpy.ndarray):
        #Handle QThread related stuff (i.e. signals and stuff here)

class QCamRecorder(QCamProcessor):

class QCamQPixmap(QCamProcessor):