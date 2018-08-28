import cv2
import numpy
import time
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage

class QCamProcessor(QObject):

    img_processed = pyqtSignal(object)
    status = pyqtSignal(str)
    is_running = pyqtSignal()
    is_processing = pyqtSignal(numpy.ndarray)

    def __init__(self):
        super().__init__()
        #self._cancel = False

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
        self.is_processing[numpy.ndarray].disconnect(self.processImg)
        #self._cancel = True

    #clean up processing, i.e. save file etc.
    def finishProcessing(self):
        self.img_processed.emit()
        return 0


class QCamRecorder(QCamProcessor):
    img_processed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.cvcodec = None #cv2.VideoWriter_fourcc()
        self.out = None #cv2.VideoWriter()

    def startProcessing(self, img_received=pyqtSignal(numpy.ndarray)):
        path = ''
        currenttime = time.strftime('%d-%m-%Y_%H-%M-%S', time.localtime())
        fimfile = path + 'FIM_' + currenttime + '.avi'

        self.cvcodec = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(fimfile, self.cvcodec, 40.0, (1200, 1200), False) #isColor=False
        super().startProcessing(img_received)


    def processImg(self, img=numpy.ndarray):
        try:
            #wird ausgeführt aber schreibt keine frames in Datei
            self.out.write(img)
        except Exception as e:
            #print("An exception occurred.")
            #print(str(e))
            self.status.emit(str(e))



    def cancelProcessing(self):
        super().cancelProcessing()
        self.finishProcessing()


    def finishProcessing(self):
        self.out.release()
        #warum hängt das?
        #self.img_processed.emit()


class QCamQPixmap(QCamProcessor):

    def processImg(self, img=numpy.ndarray):
        qimg = QImage(img, img.data.shape[0], img.data.shape[1], QImage.Format_Mono)
        qpxmp = QPixmap(qimg)
        self.img_processed.emit(qpxmp)


class QCamSnapshot(QCamProcessor):
    img_processed = pyqtSignal()

    def processImg(self, img=numpy.ndarray):
        path = ''
        currenttime = time.strftime('%d-%m-%Y_%H-%M-%S', time.localtime())
        fimfile = path + 'FIMsnapshot_' + currenttime + '.png'
        self.status.emit(fimfile)
        cv2.imwrite(fimfile, img)
        #cv2.imwrite('FIMsnapshot.png', img)
        self.cancelProcessing() #we just want to save one frame, so when we receive one, we immediately stop.
        self.finishProcessing()


