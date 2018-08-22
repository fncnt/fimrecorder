from pypylon import pylon
from pypylon import genicam
import cv2
import numpy
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread

class QCamWorker(QObject):
    #Worker for QThreads
    #This Class grabs frames in the background
    #and pushes them to other threads responsible
    #for snapshots and recording
    #using pyqtSignal and pyqtSlot passing numpy images

    _cam = pylon.InstantCamera()
    device_stopped = pyqtSignal()
    frame_grabbed = pyqtSignal(numpy.ndarray)
    is_grabbing = pyqtSignal()
    device_status = pyqtSignal(str)
    #TODO overload signal to allow integer codes
    # 0: device found, using device
    # 1: no device found

    def __init__(self):
        super().__init__()
        self.connectToCam()
        self._stop = False
        #self.device_closed.connect(self.close)

    def stop(self):
        #self.device_status.emit("Stopping frame-grabbing...")
        self._stop  = True
        #self._cam.StopGrabbing()

    @pyqtSlot()
    def connectToCam(self):
        try:
            # Create an instant camera object with the camera device found first.
            if not self._cam.IsOpen():
                self._cam = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
                #self._cam.Open()
            # Print the model name of the camera.
            print("Using device ", self._cam.GetDeviceInfo().GetModelName())
            self.device_status.emit("Using device " + self._cam.GetDeviceInfo().GetModelName())
            self._stop = False

        except genicam.GenericException as e:
            # Error handling.
            print("An exception occurred.")
            print(str(e))
            self.device_status.emit("No device found.")

    @pyqtSlot()
    def grabFrames(self):
        converter = pylon.ImageFormatConverter()
        # converting to opencv mono8/mono12 format
        converter.OutputPixelFormat = pylon.PixelType_Mono8
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        # default = 10
        self._cam.MaxNumBuffer = 10
        # self._cam.StartGrabbingMax(100)
        self._cam.StartGrabbing()

        # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
        # when c_countOfImagesToGrab images have been retrieved.
        while self._cam.IsGrabbing() and not self._stop:
            self.is_grabbing.emit()
            # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
            grabresult = self._cam.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            if grabresult.GrabSucceeded():

                # Access the image data
                image = converter.Convert(grabresult)
                img = image.GetArray()
                self.frame_grabbed.emit(img)
                self.device_status.emit(str(type(img)))
                #cv2.namedWindow('title', cv2.WINDOW_NORMAL)
                #cv2.imshow('title', img)
                #k = cv2.waitKey(1)
                #if k == 27:
                #   break

            else:
                print("Error: ", grabresult.ErrorCode, grabresult.ErrorDescription)
                self.device_status.emit("Can't grab frames from camera.")
            grabresult.Release()

        #self._cam.StopGrabbing()
        self.device_status.emit("Stopped frame-grabbing.")
        self.device_stopped.emit()
        #self._stop = False


class QCamera(QObject):
    #init camera on self.refresh()
    camThread = QThread()
    baslerace = QCamWorker()

    frame_grabbed = pyqtSignal(numpy.ndarray)
    is_grabbing = pyqtSignal()
    device_stop = pyqtSignal()
    device_status = pyqtSignal(str)
    #TODO overload signal to allow integer codes
    # 0: device found, using device
    # 1: no device found


    @pyqtSlot()
    def reset(self):
        self.baslerace.stop()
        self.baslerace.connectToCam()

    #start thread with _grab
    @pyqtSlot()
    def grabInBackground(self):
        self.baslerace.moveToThread(self.camThread)
        #connect signals
        self.baslerace.device_status.connect(self.device_status)
        self.baslerace.frame_grabbed.connect(self.frame_grabbed)
        self.baslerace.is_grabbing.connect(self.is_grabbing)

        self.baslerace.device_stopped.connect(self.camThread.quit)

        self.camThread.started.connect(self.baslerace.grabFrames)
        self.camThread.start()

    def stopGrabbing(self):
        #self.device_stop.emit()
        self.baslerace.stop()
        self.camThread.deleteLater()
        #self.camThread.wait()
        #self.camThread.exit()
