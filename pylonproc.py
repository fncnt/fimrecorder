import cv2
import numpy
import time
import os
import errno
import math
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage

class QCamProcessor(QObject):

    img_processed = pyqtSignal(object)
    status = pyqtSignal(str)
    is_running = pyqtSignal()
    is_processing = pyqtSignal(numpy.ndarray)

    def __init__(self):
        super().__init__()

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


    #when cancel signal is received
    def cancelProcessing(self):
        try:
            self.is_processing[numpy.ndarray].disconnect(self.processImg)
        except Exception as e:
            print(str(e))

    #clean up processing, i.e. save file etc.
    def finishProcessing(self):
        self.img_processed.emit()


class QCamRecorder(QCamProcessor):

    img_processed = pyqtSignal()
    fimjson_path = pyqtSignal(str)
    timelimit_reached = pyqtSignal()

    fpath = ''

    fcc = 'XVID'

    def __init__(self):
        super().__init__()
        self.cvcodec = None  # cv2.VideoWriter_fourcc()
        self.out = None  # cv2.VideoWriter()
        self.fps = 41.58177  # max. FPS
        self.maxframes = 100  # arbitrary so that we record at least something for testing purposes
        self.framecount = 0
        self.fimjson = ''

    # @pyqtSlot(float)
    def changeFps(self, newfps):
        self.fps = newfps
        self.status.emit("Will record at " + str(self.fps) + " fps.")

    def msecsToFrames(self, mseconds):
        self.maxframes = math.floor(self.fps * mseconds / 1000)  # Rounding down for consistency
        self.status.emit("Will record " + str(self.maxframes) + " frames.")

    def startProcessing(self, img_received=pyqtSignal(numpy.ndarray)):
        currenttime = time.strftime('%d-%m-%Y_%H-%M-%S', time.localtime())
        subpath = os.path.join(self.fpath, currenttime)
        if not os.path.exists(subpath):
            try:
                os.makedirs(subpath)
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        fimfile = 'FIM_' + currenttime + '.avi'
        self.fimjson = os.path.join(subpath, 'FIM_' + currenttime + '.json')

        self.cvcodec = cv2.VideoWriter_fourcc(*self.fcc)
        self.out = cv2.VideoWriter(os.path.join(subpath, fimfile), self.cvcodec, self.fps, (1200, 1200), False)  # isColor=False
        super().startProcessing(img_received)

    def processImg(self, img=numpy.ndarray):
        try:
            if self.framecount < self.maxframes:
                self.out.write(img)
                self.framecount += 1
            else:
                self.timelimit_reached.emit()
        except Exception as e:
            self.status.emit(str(e))

    def cancelProcessing(self):
        super().cancelProcessing()
        self.finishProcessing()

    def finishProcessing(self):
        self.out.release()
        self.fimjson_path.emit(self.fimjson)
        super().finishProcessing()


class QCamQPixmap(QCamProcessor):

    def processImg(self, img=numpy.ndarray):
        qimg = QImage(img, img.data.shape[0], img.data.shape[1], QImage.Format_Grayscale8)
        qpxmp = QPixmap(qimg)
        self.img_processed.emit(qpxmp)

class QCamSnapshot(QCamProcessor):
    img_processed = pyqtSignal()
    fpath = ''
    def processImg(self, img=numpy.ndarray):
        currenttime = time.strftime('%d-%m-%Y_%H-%M-%S', time.localtime())
        fimfile ='FIMsnapshot_' + currenttime + '.png'
        self.status.emit(fimfile)
        cv2.imwrite(os.path.join(self.fpath, fimfile), img)

        self.cancelProcessing()  # we just want to save one frame, so when we receive one, we immediately stop.
        self.finishProcessing()


