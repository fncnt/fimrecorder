from pypylon import pylon
from pypylon import genicam
import numpy
import cv2
import os
import logging
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread

logger = logging.getLogger(__name__)


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
    emulated = False
    threshold = 0
    cutoff = False
    bgcount = 0
    maxinbg = 100
    subtractbg = False
    stretchhistogram = False
    stretchfactor = 0.0
    # TODO overload signal to allow integer codes
    # 0: device found, using device
    # 1: no device found

    def __init__(self):
        super().__init__()
        self.connectToCam()
        self.background = numpy.zeros((self._cam.Width.Value, self._cam.Width.Value)).astype(numpy.float)
        # self.background = numpy.zeros((self._cam.Width.Value, self._cam.Width.Value)).astype(numpy.uint8)

    #check for compatible type in function
    #I'd like to avoid setters
    #but this way I don't have to  define a function for every Attribute
    @pyqtSlot(str, object)
    def setCamAttr(self, attribute: str, value):
        try:
            #setattr(self._cam, attribute, value)
            getattr(self._cam, attribute).SetValue(value)
            # self.device_status.emit(attribute + ": " + str(value))
            self.device_status.emit(attribute + ": " + getattr(self._cam, attribute).ToString())
            logger.debug(attribute + ": " + getattr(self._cam, attribute).ToString())
        except Exception as e:
            #self.device_status.emit(str(e))
            logger.exception(str(e))

    def stop(self):
        #self.device_status.emit("Stopping frame-grabbing...")
        self._cam.StopGrabbing()

    @pyqtSlot(int)
    def resetbackground(self, maxinbg=100):
        self.bgcount = 0
        self.maxinbg = maxinbg
        self.background = numpy.zeros((self._cam.Width.Value, self._cam.Width.Value)).astype(numpy.float)

    @pyqtSlot()
    def connectToCam(self):
        try:
            # Create an instant camera object with the camera device found first.
            if not self._cam.IsOpen():
                self._cam = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
                self._cam.Open()
            # Print the model name of the camera.
            logger.debug("Using device " + self._cam.GetDeviceInfo().GetModelName())
            self.device_status.emit("Using device " + self._cam.GetDeviceInfo().GetModelName())
            self.device_name.emit(self._cam.GetDeviceInfo().GetModelName())

            self.device_status.emit("Loading device configuration")
            logger.debug("Loading device configuration")
            # pylon.FeaturePersistence.Load(os.path.join(self.fpath, self.fname), self._cam.GetNodeMap(), True)
            try:
                pylon.FeaturePersistence.Load(os.path.join(self.fpath,
                                                           self._cam.GetDeviceInfo().GetModelName() + '.pfs'),
                                              self._cam.GetNodeMap(), True)
            except BaseException as e:
                pylon.FeaturePersistence.Save(os.path.join(self.fpath,
                                                           self._cam.GetDeviceInfo().GetModelName() + '.pfs'),
                                              self._cam.GetNodeMap())
                logger.error("Couldn't find NodeMap file for " + self._cam.GetDeviceInfo().GetModelName())
                logger.error("Saving default device configuration as " + self._cam.GetDeviceInfo().GetModelName() + '.pfs' )
            # Attempt to ensure realtime grabbing
            # Max == 15 for non-admin users
            # self._cam.GrabLoopThreadPriorityOverride = True
            # self._cam.InternalGrabEngineThreadPriorityOverride = True
            # self._cam.GrabLoopThreadPriority = 30
            # self._cam.InternalGrabEngineThreadPriority = 31
            # self._cam.StreamGrabber.TransferLoopThreadPriority = 32

        except genicam.GenericException as e:
            # Error handling.
            logger.exception(str(e))
            logger.debug("No device found. Make sure to use a USB3 port.")
            self.device_status.emit("No device found. Make sure to use a USB3 port.")
            self.device_name.emit("no device")
            os.environ['PYLON_CAMEMU'] = '1'
            self.emulated = True
            self.connectToCam()

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
            try:
                self.is_grabbing.emit()
                # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
                grabresult = self._cam.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

                if grabresult.GrabSucceeded():
                    # Access the image data
                    image = converter.Convert(grabresult)
                    img = image.GetArray()
                    # img = numpy.rot90(img, 1)
                    if self.subtractbg:
                        if self.bgcount < self.maxinbg:
                            #self.background = (bgcount/100) * self.background + (1 - bgcount/100) * img
                            self.background = cv2.accumulateWeighted(img.astype(numpy.float), self.background, alpha=1-self.bgcount/self.maxinbg)
                            self.bgcount += 1
                        img = cv2.subtract(img.astype(numpy.uint8), self.background.astype(numpy.uint8))
                    else:
                        self.resetbackground(self.maxinbg)
                        
                    if self.threshold > 0 and self.cutoff:
                        _, img = cv2.threshold(img, self.threshold, 255, cv2.THRESH_TOZERO)

                    if self.stretchfactor >= 0 and self.stretchhistogram:
                        img = cv2.multiply(img, img, scale=self.stretchfactor / 255)

                    self.frame_grabbed.emit(img)
                else:
                    logger.error("Error: " + grabresult.ErrorCode + grabresult.ErrorDescription)
                    logger.debug("Can't grab frames from camera.")
                    self.device_status.emit("Can't grab frames from camera.")
                grabresult.Release()
            except BaseException as e:
                logger.exception(str(e))
                logger.debug("The device has been disconnected.")
                self.device_status.emit("The device has been disconnected.")

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
        self.camThread.setPriority(QThread.TimeCriticalPriority)
        self.device_name.emit(self.baslerace._cam.GetDeviceInfo().GetModelName())

    def stopGrabbing(self):
        self.baslerace.stop()