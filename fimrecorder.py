#!/usr/bin/env python3

import sys
import os
import numpy
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem
from PyQt5.QtCore import QThread, QTime, Qt
from PyQt5.QtGui import QPixmap

from fimui import ui_fimwindow
import fakecom
import pylonproc
import settingshandler

# TODO: make this a class Fim()
# TODO: and create an object in main for readability

app = QApplication(sys.argv)
window = QMainWindow()
ui = ui_fimwindow.Ui_fimWindow()
camera = fakecom.QCamera()
disposablecam = pylonproc.QCamSnapshot()
dcthread = QThread()
recordingcam = pylonproc.QCamRecorder()
recthread = QThread()
# loads settings on __init__()
fimsettings = settingshandler.SettingsHandler()
ui.selectparamfile = QFileDialog()

speciescell = QTableWidgetItem("")
straincell = QTableWidgetItem("")
genotypecell = QTableWidgetItem("")
moreinfocell = QTableWidgetItem("")

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
    # if ui.FpsEnableChkBx.isChecked():
    ui.FpsDSpinBox.setValue(fimsettings.parameters['Frame Rate'])
    ui.RecDurTEdit.setTime(QTime.fromString(fimsettings.parameters['Recording Duration']))
    # WIP not really nice that way
    speciescell.setText(fimsettings.parameters['User Data']['Species'])
    straincell.setText(fimsettings.parameters['User Data']['Strain'])
    genotypecell.setText(fimsettings.parameters['User Data']['Genotype'])
    moreinfocell.setText(fimsettings.parameters['User Data']['More Info'])

    recordingcam.msecsToFrames(QTimeToMsecs(ui.RecDurTEdit.time()))
    recordingcam.fcc = fimsettings.settings['Video Codec']
    recordingcam.fpath = fimsettings.settings['Recording Directory']
    disposablecam.fpath = fimsettings.settings['Snapshot Directory']
    camera.baslerace.fpath = fimsettings.settings['Configuration Directory']
    camera.baslerace.fname = fimsettings.settings['Default Camera Parameters']


def pushSettings(fpath="", fname="settings.json", onlyparameters=False):
    fimsettings.parameters['Exposure Time'] = ui.ExpTimeSpinBox.value()
    # if ui.FpsEnableChkBx.isChecked():
    fimsettings.parameters['Frame Rate'] = ui.FpsDSpinBox.value()
    fimsettings.parameters['Recording Duration'] = ui.RecDurTEdit.time().toString()
    fimsettings.parameters['User Data']['Species'] = speciescell.text()
    fimsettings.parameters['User Data']['Strain'] = straincell.text()
    fimsettings.parameters['User Data']['Genotype'] = genotypecell.text()
    fimsettings.parameters['User Data']['More Info'] = moreinfocell.text()

    # temporarily
    fimsettings.saveSettings(fpath, fname, onlyparameters)

# TODO: Better error handling
def openParamFile():
    ui.selectparamfile.setAcceptMode(QFileDialog.AcceptOpen)
    try:
        completepath = ui.selectparamfile.getOpenFileName(ui.selectparamfile, 'Open Parameter File',
                                                      fimsettings.settings['Recording Directory'],
                                                      '*.json')[0]
        fpath = os.path.dirname(completepath)
        fname = os.path.basename(completepath)
        fimsettings.loadSettings(fpath, fname, True)
        pullSettings()
    except Exception as e:
        print(str(e))

# TODO: Better error handling
def writeParamFile():
    ui.selectparamfile.setAcceptMode(QFileDialog.AcceptSave)
    try:
        completepath = ui.selectparamfile.getSaveFileName(ui.selectparamfile, 'Save Parameter File',
                                                      fimsettings.settings['Recording Directory'],
                                                      '*.json')[0]
        fpath = os.path.dirname(completepath)
        fname = os.path.basename(completepath)
        fimsettings.saveSettings(fpath, fname, True)
    except Exception as e:
        print(str(e))


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
    recordingcam.fimjson_path[str].connect(lambda val: pushSettings(os.path.dirname(val),
                                                                    os.path.basename(val),
                                                                    True
                                                                    )
                                           )
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
    # Doesn't work without lambda? o.ô
    ui.FpsDSpinBox.valueChanged[float].connect(lambda val: recordingcam.changeFps(val))
    ui.RecDurTEdit.timeChanged.connect(lambda val: recordingcam.msecsToFrames(QTimeToMsecs(val)))
    app.aboutToQuit.connect(pushSettings)


def disableUiElements():
    ui.ExpAutoChkBx.setDisabled(True)
    ui.actionRefresh.setDisabled(True)
    ui.actionSnapshot.setDisabled(True)
    #ui.previewLabel.close()
    #ui.camView.close()


def main():
    ui.setupUi(window)
    # for some reason QT Designer doesn't apply this on its own
    # 1 = MinuteSection
    ui.RecDurTEdit.setCurrentSectionIndex(1)
    ui.UserDataTable.setItem(-1, 1, speciescell)
    ui.UserDataTable.setItem(0, 1, straincell)
    ui.UserDataTable.setItem(1, 1, genotypecell)
    ui.UserDataTable.setItem(2, 1, moreinfocell)

    # Disable UI elements that don't work yet
    disableUiElements()
    recordingcam.moveToThread(recthread)
    # more refined logic needed here to improve UX
    # if camera.baslerace._cam.IsOpen():
    #    camera.grabInBackground()
    # Handles interaction between UI and cam stuff
    connectSignals()
    # fakecom specific code:
    camera.grabInBackground()
    # pull settings into cam classes and UI
    pullSettings()

    previewcam = pylonproc.QCamQPixmap()
    pcthread = QThread()
    previewcam.moveToThread(pcthread)
    ui.camView.setAlignment(Qt.AlignCenter)
    ui.camView.setScaledContents(True)
    #camera.frame_grabbed[numpy.ndarray].connect(previewcam.processImg)
    pcthread.started.connect(lambda: previewcam.startProcessing(camera.frame_grabbed))
    previewcam.img_processed.connect(lambda qpxmp: ui.camView.setPixmap(qpxmp.scaled(ui.camView.size(),
                                                                                     Qt.KeepAspectRatio,
                                                                                     Qt.FastTransformation)))
    # previewcam.img_processed.connect(ui.camView.setPixmap)
    # previewcam.img_processed.connect(lambda discard: print(ui.camView.size()))

    pcthread.start()
    app.aboutToQuit.connect(pcthread.exit)

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
