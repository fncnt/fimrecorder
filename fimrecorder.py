#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, QTime
from PyQt5.QtGui import QPixmap

from fimui import ui_fimwindow
import pyloncom
import pylonproc
import settingshandler
def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = ui_fimwindow.Ui_fimWindow()
    ui.setupUi(window)

    # try loading parameters on startup on __init__()
    fimsettings = settingshandler.SettingsHandler()
    # pull Settings into program
    def pullSettings():
        ui.ExpTimeSpinBox.setValue(fimsettings.parameters['Exposure Time'])
        if ui.FpsEnableChkBx.isChecked():
            ui.FpsDSpinBox.setValue(fimsettings.parameters['Frame Rate'])
        #ui.RecDurTEdit.dateTimeFromText(fimsettings.parameters['Recording Duration'])

    pullSettings()
    # Save settings automatically on exit
    app.aboutToQuit.connect(fimsettings.saveSettings)
    # manually load settings via button (for reproducible measurements
    #ui.actionLoad_Parameters.connect(fimsettings.)
    # QFileDialog needed

    # for some reason QT Designer doesn't apply this on its own
    # 1 = MinuteSection
    ui.RecDurTEdit.setCurrentSectionIndex(1)

    camera = pyloncom.QCamera()
    camera.device_status[str].connect(ui.statusbar.showMessage)
    camera.device_status[str].connect(print)

    if camera.baslerace._cam.IsOpen():
        camera.grabInBackground()
    #camera.is_grabbing.connect(lambda: ui.statusbar.showMessage("grabbing..."))

    ui.actionRefresh.triggered.connect(camera.reset)
    #Replace lambda by functools.partial?
    ui.ExpTimeSpinBox.valueChanged[int].connect(
        lambda val: camera.baslerace.setCamAttr('ExposureTime', val)
    )
    ui.ExpTimeSpinBox.valueChanged[int].connect(
        lambda val: fimsettings.parameters.__setitem__('Exposure Time', val)
    )

    #Doesn't work yet
    def toggleExposureAuto(on: bool):
        if on:
            #Apparantly setattr() doesn't do any type conversion as = does?
            #camera.baslerace.setCamAttr('ExposureAuto', 'ExposureAuto_Continuous')
            camera.baslerace._cam.ExposureAuto = 'ExposureAuto_Continuous'
            #camera.baslerace._cam.ExposureAuto.SetValue('ExposureAuto_Continuous')
        else:
            #camera.baslerace.setCamAttr('ExposureAuto', 'ExposureAuto_Off')
            camera.baslerace._cam.ExposureAuto = 'ExposureAuto_Off'
    ui.ExpAutoChkBx.toggled[bool].connect(toggleExposureAuto)

    ui.FpsEnableChkBx.toggled[bool].connect(
        #lambda val: camera.baslerace.setCamAttr('AcquisitionFrameRateEnable	', int(val))
        lambda val: camera.baslerace._cam.AcquisitionFrameRateEnable.SetValue(int(val))
    )

    ui.FpsDSpinBox.valueChanged[float].connect(
        lambda val: camera.baslerace.setCamAttr('AcquisitionFrameRate', val)
    )

    disposablecam = pylonproc.QCamSnapshot()
    dcthread = QThread()
    def saveSnapshot():
        disposablecam.moveToThread(dcthread)

        disposablecam.status[str].connect(print)
        dcthread.started.connect(lambda: disposablecam.startProcessing(camera.frame_grabbed))
        dcthread.start()
        disposablecam.img_processed.connect(dcthread.quit)

    ui.actionSnapshot.triggered.connect(saveSnapshot)

    def QTimeToMsecs(time: QTime):
        msecs = 0
        msecs += time.msec()
        msecs += time.second() * 1000
        msecs += time.minute() * 1000 * 60
        msecs += time.hour() * 1000 * 60 * 60
        return msecs

    recordingcam = pylonproc.QCamRecorder()
    recordingcam.status.connect(print)
    ui.FpsDSpinBox.valueChanged[float].connect(recordingcam.changeFps)
    ui.RecDurTEdit.timeChanged.connect(lambda val: recordingcam.msecsToFrames(QTimeToMsecs(val)))
    recordingcam.timelimit_reached.connect(ui.actionRecord.toggle)
    recthread = QThread()
    recordingcam.moveToThread(recthread)


    def recordVideo(toggled=bool):
        if toggled:
            #make sure framecount is zero so we record everything we want:
            recordingcam.framecount = 0

            recthread.start()
            recordingcam.startProcessing(camera.frame_grabbed)
        else:
            recordingcam.cancelProcessing()
            # Does terminate without blocking main thread.
            # Also it's actually not recommended.
            recthread.terminate()
            #recthread.quit()
            #recthread.wait(100)

    ui.actionRecord.toggled[bool].connect(recordVideo)

    #previewthread = QThread()
    #ui.camView.moveToThread(previewthread)
    #previewthread.start()

    #previewcam = pylonproc.QCamQPixmap()
    #pcthread = QThread()
    #previewcam.moveToThread(pcthread)
    #previewcam.img_processed.connect(ui.camView.setPixmap)
    #camera.frame_grabbed[numpy.ndarray].connect(previewcam.processImg)
    #pcthread.started.connect(lambda: previewcam.startProcessing(camera.frame_grabbed))
    #pcthread.start()
    #ui.camView.setScaledContents(True)

    window.show()
    sys.exit(app.exec_())





if __name__ == "__main__":
    main()
