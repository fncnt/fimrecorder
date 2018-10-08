from pypylon import pylon
from pypylon import genicam
import numpy
import os
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread


class QCamWorker(QObject):
    # Worker for QThreads
    # This Class grabs frames in the background
    # and pushes them to other threads responsible
    # for snapshots and recording
    # using pyqtSignal and pyqtSlot passing numpy images

    fpath = 'config'
    fname = 'FIM_NodeMap.pfs'

    _cam = pylon.InstantCamera()
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

    #check for compatible type in function
    #I'd like to avoid setters
    #but this way I don't have to  define a function for every Attribute
    @pyqtSlot(str, object)
    def setCamAttr(self, attribute: str, value):
        try:
            setattr(self._cam, attribute, value)
            self.device_status.emit(attribute + ": " + str(value))
        except Exception as e:
            self.device_status.emit(str(e))

    def stop(self):
        #self.device_status.emit("Stopping frame-grabbing...")
        self._cam.StopGrabbing()

    @pyqtSlot()
    def connectToCam(self):
        try:
            # Create an instant camera object with the camera device found first.
            if not self._cam.IsOpen():
                self._cam = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
                self._cam.Open()
            # Print the model name of the camera.
            print("Using device ", self._cam.GetDeviceInfo().GetModelName())
            self.device_status.emit("Using device " + self._cam.GetDeviceInfo().GetModelName())
            self.device_name.emit(self._cam.GetDeviceInfo().GetModelName())

            self.device_status.emit("Loading device configuration")
            pylon.FeaturePersistence.Load(os.path.join(self.fpath, self.fname), self._cam.GetNodeMap(), True)

        except genicam.GenericException as e:
            # Error handling.
            print("An exception occurred.")
            print(str(e))
            self.device_status.emit("No device found.")
            self.device_name.emit("no device")


    @pyqtSlot()
    def grabFrames(self):
        converter = pylon.ImageFormatConverter()
        # converting to opencv mono8/mono12 format

        converter.OutputPixelFormat = pylon.PixelType_Mono8
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        # default = 10
        self._cam.MaxNumBuffer = 10
        self._cam.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) #or GrabStrategy_OneByOne

        while self._cam.IsGrabbing():
            self.is_grabbing.emit()
            # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
            grabresult = self._cam.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            if grabresult.GrabSucceeded():
                # Access the image data
                image = converter.Convert(grabresult)
                img = image.GetArray()
                # img = numpy.rot90(img, 1)
                self.frame_grabbed.emit(img)
            else:
                print("Error: ", grabresult.ErrorCode, grabresult.ErrorDescription)
                self.device_status.emit("Can't grab frames from camera.")
            grabresult.Release()

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
        self.camThread.start()
        self.device_name.emit(self.baslerace._cam.GetDeviceInfo().GetModelName())

    def stopGrabbing(self):
        self.baslerace.stop()