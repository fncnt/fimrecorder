#!/usr/bin/env python3

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import QThread, QTime
from PyQt5.QtGui import QPixmap

from fimui import ui_fimwindow
import pyloncom
import pylonproc
import settingshandler

# TODO: make this a class Fim()
# TODO: and create an object in main for readability
# TODO: or define variables globally


app = QApplication(sys.argv)
window = QMainWindow()
ui = ui_fimwindow.Ui_fimWindow()
camera = pyloncom.QCamera()
disposablecam = pylonproc.QCamSnapshot()
dcthread = QThread()
recordingcam = pylonproc.QCamRecorder()
recthread = QThread()
# loads settings on __init__()
fimsettings = settingshandler.SettingsHandler()
ui.selectparamfile = QFileDialog()

def QTimeToMsecs(time: QTime):
    msecs = 0
    msecs += time.msec()
    msecs += time.second() * 1000
    msecs += time.minute() * 1000 * 60
    msecs += time.hour() * 1000 * 60 * 60
    return msecs


# Doesn't work yet
def toggleExposureAuto(on: bool):
    if on:
        # Apparantly setattr() doesn't do any type conversion as = does?
        # camera.baslerace.setCamAttr('ExposureAuto', 'ExposureAuto_Continuous')
        camera.baslerace._cam.ExposureAuto = 'ExposureAuto_Continuous'
        # camera.baslerace._cam.ExposureAuto.SetValue('ExposureAuto_Continuous')
    else:
        # camera.baslerace.setCamAttr('ExposureAuto', 'ExposureAuto_Off')
        camera.baslerace._cam.ExposureAuto = 'ExposureAuto_Off'


def saveSnapshot():
    disposablecam.moveToThread(dcthread)

    dcthread.started.connect(lambda: disposablecam.startProcessing(camera.frame_grabbed))
    dcthread.start()
    disposablecam.img_processed.connect(dcthread.quit)


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
        # recthread.quit()
        # recthread.wait(100)


def pullSettings():
    ui.ExpTimeSpinBox.setValue(fimsettings.parameters['Exposure Time'])
    if ui.FpsEnableChkBx.isChecked():
        ui.FpsDSpinBox.setValue(fimsettings.parameters['Frame Rate'])
    ui.RecDurTEdit.setTime(QTime.fromString(fimsettings.parameters['Recording Duration']))

    recordingcam.fcc = fimsettings.settings['Video Codec']
    recordingcam.fpath = fimsettings.settings['Recording Directory']
    disposablecam.fpath = fimsettings.settings['Snapshot Directory']
    camera.baslerace.fpath = fimsettings.settings['Configuration Directory']
    camera.baslerace.fname = fimsettings.settings['Default Camera Parameters']


def pushSettings(fpath="", fname="settings.json", onlyparameters=False):
    fimsettings.parameters['Exposure Time'] = ui.ExpTimeSpinBox.value()
    if ui.FpsEnableChkBx.isChecked():
        fimsettings.parameters['Frame Rate'] = ui.FpsDSpinBox.value()
    fimsettings.parameters['Recording Duration'] = ui.RecDurTEdit.time().toString()
    # temporaily
    fimsettings.saveSettings(fpath, fname, onlyparameters)


def openParamFile():
    ui.selectparamfile.setAcceptMode(QFileDialog.AcceptOpen)
    completepath = ui.selectparamfile.getOpenFileName(ui.selectparamfile, 'Open Parameter File',
                                                      fimsettings.settings['Recording Directory'],
                                                      '*.json')[0]
    fpath = os.path.dirname(completepath)
    fname = os.path.basename(completepath)
    fimsettings.loadSettings(fpath, fname, True)
    pullSettings()


def writeParamFile():
    ui.selectparamfile.setAcceptMode(QFileDialog.AcceptSave)
    completepath = ui.selectparamfile.getSaveFileName(ui.selectparamfile, 'Save Parameter File',
                                                      fimsettings.settings['Recording Directory'],
                                                      '*.json')[0]
    fpath = os.path.dirname(completepath)
    fname = os.path.basename(completepath)
    fimsettings.saveSettings(fpath, fname, True)


def connectSignals():
    # Print messages to statusbar and console
    camera.device_status[str].connect(ui.statusbar.showMessage)
    camera.device_status[str].connect(print)
    disposablecam.status[str].connect(print)
    recordingcam.status[str].connect(print)

    # Handle QActions
    ui.actionSnapshot.triggered.connect(saveSnapshot)
    ui.actionRefresh.triggered.connect(camera.reset)
    ui.actionRecord.toggled[bool].connect(recordVideo)
    ui.actionLoad_Parameters.triggered.connect(openParamFile)
    ui.actionSave_Parameters.triggered.connect(writeParamFile)
    # Handle pyloncom & pylonproc signals
    recordingcam.timelimit_reached.connect(ui.actionRecord.toggle)
    # Connect widgets to cam classes and SettingsHandler
    # Replace lambda by functools.partial?
    ui.ExpTimeSpinBox.valueChanged[int].connect(
        lambda val: camera.baslerace.setCamAttr('ExposureTime', val)
    )
    ui.ExpTimeSpinBox.valueChanged[int].connect(
        lambda val: fimsettings.parameters.__setitem__('Exposure Time', val)
    )
    # camera.is_grabbing.connect(lambda: ui.statusbar.showMessage("grabbing..."))
    ui.ExpAutoChkBx.toggled[bool].connect(toggleExposureAuto)
    ui.FpsEnableChkBx.toggled[bool].connect(
        # lambda val: camera.baslerace.setCamAttr('AcquisitionFrameRateEnable	', int(val))
        lambda val: camera.baslerace._cam.AcquisitionFrameRateEnable.SetValue(int(val))
    )
    ui.FpsDSpinBox.valueChanged[float].connect(
        lambda val: camera.baslerace.setCamAttr('AcquisitionFrameRate', val)
    )
    ui.FpsDSpinBox.valueChanged[float].connect(recordingcam.changeFps)
    ui.RecDurTEdit.timeChanged.connect(lambda val: recordingcam.msecsToFrames(QTimeToMsecs(val)))
    app.aboutToQuit.connect(pushSettings)


def disableUiElements():
    ui.ExpAutoChkBx.setDisabled(True)
    ui.actionRefresh.setDisabled(True)
    ui.actionSnapshot.setDisabled(True)
    ui.previewLabel.close()
    ui.camView.close()

def main():
    ui.setupUi(window)
    # for some reason QT Designer doesn't apply this on its own
    # 1 = MinuteSection
    ui.RecDurTEdit.setCurrentSectionIndex(1)
    # Disable UI elements that don't work yet
    disableUiElements()
    recordingcam.moveToThread(recthread)
    # more refined logic needed here to improve UX
    if camera.baslerace._cam.IsOpen():
        camera.grabInBackground()
    # Handles interaction between UI and cam stuff
    connectSignals()
    # pull settings into cam classes and UI
    pullSettings()
    # previewthread = QThread()
    # ui.camView.moveToThread(previewthread)
    # previewthread.start()
    # previewcam = pylonproc.QCamQPixmap()
    # pcthread = QThread()
    # previewcam.moveToThread(pcthread)
    # previewcam.img_processed.connect(ui.camView.setPixmap)
    # camera.frame_grabbed[numpy.ndarray].connect(previewcam.processImg)
    # pcthread.started.connect(lambda: previewcam.startProcessing(camera.frame_grabbed))
    # pcthread.start()
    # ui.camView.setScaledContents(True)

    # manually load settings via button (for reproducible measurements
    # ui.actionLoad_Parameters.connect(fimsettings.)
    # QFileDialog needed

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
