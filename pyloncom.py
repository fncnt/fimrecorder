from pypylon import pylon
from pypylon import genicam
import cv2
from threading import Thread
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread

class QCamWorker(QObject):
    #Worker for QThreads
    #This Class grabs frames in the background
    #and pushes them to other threads responsible
    #for snapshots and recording
    #using pyqtSignal and pyqtSlot passing numpy images

    _cam = pylon.InstantCamera()
    device_closed = pyqtSignal()
    frame_grabbed = pyqtSignal()
    is_grabbing = pyqtSignal()
    device_status = pyqtSignal(str)
    #TODO overload signal to allow integer codes
    # 0: device found, using device
    # 1: no device found


    def __init__(self):
        super().__init__()
        self.connectToCam()
        self._stop = False
        self.device_closed.connect(self.close)

    def stop(self):
        self.device_status.emit("Stopping frame-grabbing...")
        self._stop = True

    def close(self):
        self._stop = False
        self._cam.Close()

    @pyqtSlot()
    def connectToCam(self):
        try:
            # Create an instant camera object with the camera device found first.
            self._cam = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
            if not self._cam.IsOpen():
                self._cam.Open()
            # Print the model name of the camera.
            print("Using device ", self._cam.GetDeviceInfo().GetModelName())
            self.device_status.emit("Using device " + self._cam.GetDeviceInfo().GetModelName())

        except genicam.GenericException as e:
            # Error handling.
            print("An exception occurred.")
            print(str(e))
            self.device_status.emit("No device found.")

    @pyqtSlot()
    def grabFrames(self):
        converter = pylon.ImageFormatConverter()
        # converting to opencv bgr format
        converter.OutputPixelFormat = pylon.PixelType_Mono8
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        # default = 10
        self._cam.MaxNumBuffer = 10
        # self._cam.StartGrabbingMax(100)
        self._cam.StartGrabbing()

        # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
        # when c_countOfImagesToGrab images have been retrieved.
        while self._cam.IsGrabbing():
            if self._stop:
                self.device_status.emit("Stopped frame-grabbing.")
                self.device_closed.emit()
                break
            self.is_grabbing.emit()
            # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
            grabresult = self._cam.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            # Image grabbed successfully?
            if grabresult.GrabSucceeded():
                # Access the image data.
                self.frame_grabbed.emit()
                #print("SizeX: ", grabresult.Width)
                #print("SizeY: ", grabresult.Height)
                #img = grabresult.Array
                #print("Gray value of first pixel: ", img[0, 0])

                # Access the image data
                # image = converter.Convert(grabResult)
                # img = image.GetArray()
                # cv2.namedWindow('title', cv2.WINDOW_NORMAL)
                # cv2.imshow('title', img)
                # k = cv2.waitKey(1)
                # if k == 27:
                #    break
            else:
                print("Error: ", grabresult.ErrorCode, grabresult.ErrorDescription)
                self.device_status.emit("Can't grab frames from camera.")
            grabresult.Release()



class QCamera(QObject):
    #init camera on self.refresh()
    camThread = QThread()
    baslerace = QCamWorker()

    frame_grabbed = pyqtSignal()
    is_grabbing = pyqtSignal()
    device_stop = pyqtSignal()
    device_status = pyqtSignal(str)
    #TODO overload signal to allow integer codes
    # 0: device found, using device
    # 1: no device found


    @pyqtSlot()
    def refresh(self):
        self.baslerace.close()
        self.baslerace.connectToCam()

    #worker method for qthread


    #start thread with _grab
    @pyqtSlot()
    def grabInBackground(self):
        self.baslerace.moveToThread(self.camThread)
        #connect signals
        self.baslerace.device_status.connect(self.device_status)
        self.baslerace.frame_grabbed.connect(self.frame_grabbed)
        self.baslerace.is_grabbing.connect(self.is_grabbing)

        self.device_stop.connect(self.baslerace.stop)

        self.camThread.started.connect(self.baslerace.grabFrames)
        self.camThread.start()

    def stopGrabbing(self):
        self.device_stop.emit()
