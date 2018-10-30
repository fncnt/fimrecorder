#!/usr/bin/env python3

import sys
import os
import math
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QVBoxLayout
from PyQt5.QtCore import QThread, QTime, pyqtSlot
from fimui import ui_fimwindow
import pyloncom
import pylonproc
import settingshandler
import logging.config

# TODO: make this a class Fim()
# TODO: and create an object in main for readability

app = QApplication(sys.argv)
window = QMainWindow()
ui = ui_fimwindow.Ui_fimWindow()
camera = pyloncom.QCamera()
disposablecam = pylonproc.QCamSnapshot()
recordingcam = pylonproc.QCamRecorder()
previewcam = pylonproc.QCamGLPreview()

dcthread = QThread()
recthread = QThread()
pcthread = QThread()
# loads settings on __init__()
fimsettings = settingshandler.SettingsHandler()

with open(os.path.join(fimsettings.settings['Configuration Directory'],
                       fimsettings.settings['Logging Configuration'])) as f:
    logging.config.dictConfig(json.load(f))
logger = logging.getLogger(__name__)


ui.selectparamfile = QFileDialog()
ui.selectparamfile.setWindowFilePath(os.path.dirname(fimsettings.settings['Recording Directory']))
# TODO: use list and/or iterator for automation
speciescell = QTableWidgetItem("")
straincell = QTableWidgetItem("")
genotypecell = QTableWidgetItem("")
experimentcell = QTableWidgetItem("")
testcondcell = QTableWidgetItem("")
moreinfocell = QTableWidgetItem("")


def bootstrapCam():
    # camera.__init__()
    # more refined logic needed here to improve UX
    if camera.baslerace._cam.IsOpen():
        try:
            camera.grabInBackground()
        except BaseException as e:
            logger.exception(str(e))

def QTimeToMsecs(time: QTime):
    msecs = 0
    msecs += time.msec()
    msecs += time.second() * 1000
    msecs += time.minute() * 1000 * 60
    msecs += time.hour() * 1000 * 60 * 60
    return msecs


# little helper so we can safely disconnect is_grabbing from setting ExpTimeSpinBox
# without disconnecting all slots.
@pyqtSlot()
def updateExpTimeSpinbox():
    ui.ExpTimeSpinBox.setValue(camera.baslerace._cam.ExposureTime.GetValue())


def toggleExposureAuto(on: bool):
    if on:
        camera.baslerace.setCamAttr('ExposureAuto', 'Continuous')
        camera.is_grabbing.connect(updateExpTimeSpinbox)
        ui.ExpTimeSpinBox.valueChanged[int].disconnect()
    else:
        camera.baslerace.setCamAttr('ExposureAuto', 'Off')
        # copied from connectSignals()
        # better remove duplicate code
        # Replace lambda by functools.partial?
        camera.is_grabbing.disconnect(updateExpTimeSpinbox)
        ui.ExpTimeSpinBox.valueChanged[int].connect(
            lambda val: camera.baslerace.setCamAttr('ExposureTime', val)
        )
        ui.ExpTimeSpinBox.valueChanged[int].connect(
            lambda val: fimsettings.parameters.__setitem__('Exposure Time', val)
        )


def saveSnapshot():
    disposablecam.moveToThread(dcthread)

    dcthread.started.connect(lambda: disposablecam.startProcessing(camera.frame_grabbed))
    dcthread.start()
    dcthread.setPriority(QThread.LowPriority)
    disposablecam.img_processed.connect(dcthread.quit)


def recordVideo(toggled=bool):
    ui.progressBar.setEnabled(toggled)
    if toggled:
        #make sure framecount is zero so we record everything we want:
        recordingcam.framecount = 0

        recthread.start()
        recthread.setPriority(QThread.TimeCriticalPriority)
        recordingcam.startProcessing(camera.frame_grabbed)
        ui.actionRecord.setText('Cancel')
        ui.progressBar.setMaximum(recordingcam.maxframes)
    else:
        recordingcam.cancelProcessing()
        # Does terminate without blocking main thread.
        # Also it's actually not recommended.
        # recthread.terminate()
        recthread.quit()
        # recthread.exit(0)
        # recthread.wait(100)
        # recthread.wait(100)
        ui.actionRecord.setText('Record')
        ui.progressBar.setValue(0)
        ui.progressBar.setMaximum(100)
        ui.progressBar.setMinimum(0)


# TODO: use iterator?
def pullSettings():
    ui.ExpTimeSpinBox.setValue(fimsettings.parameters['Exposure Time'])
    # if ui.FpsEnableChkBx.isChecked():
    ui.FpsDSpinBox.setValue(fimsettings.parameters['Frame Rate'])
    ui.GammaDSpinBox.setValue(fimsettings.parameters['Gamma Correction'])
    ui.RecDurTEdit.setTime(QTime.fromString(fimsettings.parameters['Recording Duration']))
    # WIP not really nice that way
    # use list/iterator and apply try-blocks to each cell
    speciescell.setText(fimsettings.parameters['User Data']['Species'])
    straincell.setText(fimsettings.parameters['User Data']['Strain'])
    genotypecell.setText(fimsettings.parameters['User Data']['Genotype'])
    try:
        experimentcell.setText(fimsettings.parameters['User Data']['Experiment'])
    except KeyError as ke:
        logger.error("Missing user data key " + str(ke) + ". Leaving corresponding field empty.")
    try:
        testcondcell.setText(fimsettings.parameters['User Data']['Test Conditions'])
    except KeyError as ke:
        logger.error("Missing user data key " + str(ke) + ". Leaving corresponding field empty.")
    moreinfocell.setText(fimsettings.parameters['User Data']['More Info'])

    recordingcam.msecsToFrames(QTimeToMsecs(ui.RecDurTEdit.time()))
    recordingcam.codec = fimsettings.settings['Video Codec']
    recordingcam.fpath = fimsettings.settings['Recording Directory']
    disposablecam.fpath = fimsettings.settings['Snapshot Directory']
    camera.baslerace.fpath = fimsettings.settings['Configuration Directory']
    camera.baslerace.fname = fimsettings.settings['Default Camera Parameters']


def pushSettings(fpath="", fname="settings.json", onlyparameters=False):
    fimsettings.parameters['Exposure Time'] = ui.ExpTimeSpinBox.value()
    # if ui.FpsEnableChkBx.isChecked():
    fimsettings.parameters['Frame Rate'] = ui.FpsDSpinBox.value()
    fimsettings.parameters['Gamma Correction'] = ui.GammaDSpinBox.value()
    fimsettings.parameters['Recording Duration'] = ui.RecDurTEdit.time().toString()
    fimsettings.parameters['User Data']['Species'] = speciescell.text()
    fimsettings.parameters['User Data']['Strain'] = straincell.text()
    fimsettings.parameters['User Data']['Genotype'] = genotypecell.text()
    fimsettings.parameters['User Data']['Experiment'] = experimentcell.text()
    fimsettings.parameters['User Data']['Test Conditions'] = testcondcell.text()
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
        logger.exception(str(e))

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
        logger.exception(str(e))


def connectSignals():
    # Print messages to statusbar and console
    camera.device_status[str].connect(ui.statusbar.showMessage)
    #camera.device_status[str].connect(print)
    camera.device_name[str].connect(lambda val: ui.camLabel.setText("Preview (" + val + "):"))
    #disposablecam.status[str].connect(print)
    #recordingcam.status[str].connect(print)

    # Handle QActions
    ui.actionSnapshot.triggered.connect(saveSnapshot)
    ui.actionRefresh.triggered.connect(bootstrapCam)
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
    recordingcam.frame_written.connect(lambda: ui.progressBar.setValue(recordingcam.framecount))
    recordingcam.frame_written.connect(lambda: ui.progressBar.setFormat(QTime.fromMSecsSinceStartOfDay(
        math.floor(recordingcam.framecount /
                   recordingcam.fps *
                   1000)).toString()))

    app.aboutToQuit.connect(pcthread.exit)
    pcthread.started.connect(lambda: previewcam.startProcessing(camera.frame_grabbed))
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
        lambda val: camera.baslerace.setCamAttr('AcquisitionFrameRateEnable', int(val))
    )
    ui.FpsDSpinBox.valueChanged[float].connect(
        lambda val: camera.baslerace.setCamAttr('AcquisitionFrameRate', val)
    )
    ui.GammaDSpinBox.valueChanged[float].connect(
        lambda val: camera.baslerace.setCamAttr('Gamma', val)
    )
    # Doesn't work without lambda? o.ô
    ui.FpsDSpinBox.valueChanged[float].connect(lambda val: recordingcam.changeFps(val))
    # Update recording duration when fps gets changed
    ui.FpsDSpinBox.valueChanged.connect(lambda val: recordingcam.msecsToFrames(QTimeToMsecs(ui.RecDurTEdit.time())))
    ui.RecDurTEdit.timeChanged.connect(lambda val: recordingcam.msecsToFrames(QTimeToMsecs(val)))
    app.aboutToQuit.connect(pushSettings)


def disableUiElements():
    # ui.ExpAutoChkBx.setDisabled(True)
    ui.actionRefresh.setDisabled(True)
    ui.actionRefresh.setVisible(False)
    ui.menubar.close()


def renderPreview():
    previewcam.moveToThread(pcthread)
    pcthread.start()
    pcthread.setPriority(QThread.HighPriority)


def main():
    logger.debug("Starting new session.")
    ui.setupUi(window)
    # set up OpenGL preview
    ui.camWidget.setLayout(QVBoxLayout())
    ui.camWidget.layout().addWidget(previewcam.canvas.native)

    QThread.currentThread().setPriority(QThread.HighPriority)
    # for some reason QT Designer doesn't apply this on its own
    # 1 = MinuteSection
    ui.RecDurTEdit.setCurrentSectionIndex(1)
    # TODO: don't hardcode this. Use list and/or iterator
    ui.UserDataTable.setItem(-1, 1, speciescell)
    ui.UserDataTable.setItem(0, 1, straincell)
    ui.UserDataTable.setItem(1, 1, genotypecell)
    ui.UserDataTable.setItem(2, 1, experimentcell)
    ui.UserDataTable.setItem(3, 1, testcondcell)
    ui.UserDataTable.setItem(4, 1, moreinfocell)

    # Disable UI elements that don't work yet
    disableUiElements()
    # window.showMaximized()
    # window.showNormal()
    recordingcam.moveToThread(recthread)

    # Handles interaction between UI and cam stuff
    connectSignals()
    # Start grabbing if cam is available
    # handle missing devices and try to reload.
    bootstrapCam()
    # render Preview
    renderPreview()
    # pull settings into cam classes and UI
    pullSettings()

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
