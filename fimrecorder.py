#!/usr/bin/env python3

import sys
import os
import subprocess
import math
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QVBoxLayout
from PyQt5.QtCore import QThread, QTime, pyqtSlot, QFileSystemWatcher
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
extractcam = pylonproc.QCamExtract()

dcthread = QThread()
recthread = QThread()
pcthread = QThread()
ecthread = QThread()
# loads settings on __init__()
fimsettings = settingshandler.SettingsHandler()
settingswatchdog = QFileSystemWatcher()
EXPOSURETIME = 'ExposureTime'
ACQUISITIONFRAMERATE = 'AcquisitionFrameRate'

with open(os.path.join(fimsettings.settings['Configuration Directory'],
                       fimsettings.settings['Logging Configuration'])) as f:
    logging.config.dictConfig(json.load(f))
logger = logging.getLogger(__name__)


ui.selectparamfile = QFileDialog()
ui.selectparamfile.setWindowFilePath(os.path.dirname(fimsettings.settings['Recording Directory']))
ui.selectvideofile = QFileDialog()
ui.selectvideofile.setWindowFilePath(os.path.dirname(fimsettings.settings['Recording Directory']))
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


def recordVideo(toggled: bool):
    ui.progressBar.setEnabled(toggled)
    if toggled:
        #make sure framecount is zero so we record everything we want:
        recordingcam.framecount = 0
        recordingcam.resolution = (camera.baslerace._cam.Width.Value, camera.baslerace._cam.Height.Value)
        recthread.start()
        recthread.setPriority(QThread.TimeCriticalPriority)
        recordingcam.startProcessing(camera.frame_grabbed)
        ui.actionRecord.setText('Cancel')
        ui.progressBar.setMinimum(0)
        ui.progressBar.setValue(0)
        ui.progressBar.setMaximum(recordingcam.maxframes)
    else:
        recordingcam.cancelProcessing()
        # Does terminate without blocking main thread.
        # Also it's actually not recommended.
        recthread.terminate()
        # recthread.quit()
        # recthread.exit(0)
        # recthread.wait(100)
        # recthread.wait(100)
        ui.actionRecord.setText('Record')
        #ui.progressBar.setValue(0)
        #ui.progressBar.setMaximum(100)
        #ui.progressBar.setMinimum(0)
        #ui.progressBar.setFormat("")


def extractFrames(toggled: bool):
    ui.progressBar.setEnabled(toggled)
    if toggled:
        extractcam.framesmodulo = ui.FramesModuloSpinBox.value()
        ecthread.started.connect(extractcam.startProcessing)
        ui.selectvideofile.setAcceptMode(QFileDialog.AcceptOpen)
        ui.selectvideofile.setFileMode(QFileDialog.ExistingFile)
        completepath = ''
        try:
            completepath = ui.selectvideofile.getOpenFileName(ui.centralwidget, 'Open Video File',
                                                              fimsettings.settings['Recording Directory'],
                                                              initialFilter='Video *.avi, *.mp4 (*.avi *.mp4)',
                                                              filter='Video *.avi, *.mp4 (*.avi *.mp4);;All Files (*.*)')[0]
        except Exception as e:
            logger.exception(str(e))
        if completepath == '':
            ui.actionExtract_Frames_from_Video.toggle()
        else:
            extractcam.completepath = completepath
            extractcam.framecount = 0
            ecthread.setPriority(QThread.LowPriority)
            ecthread.start()
            ui.actionExtract_Frames_from_Video.setText('Cancel Extraction')
            ui.progressBar.setMinimum(0)
            ui.progressBar.setValue(0)

    else:
        extractcam.cancelProcessing()
        ecthread.started.disconnect(extractcam.startProcessing)
        # Does terminate without blocking main thread.
        # Also it's actually not recommended.
        #recthread.terminate()
        ecthread.quit()
        # recthread.exit(0)
        # recthread.wait(100)
        # recthread.wait(100)
        ui.actionExtract_Frames_from_Video.setText('Extract Frames from AVI')
        #ui.progressBar.setValue(0)
        #ui.progressBar.setMaximum(100)
        #ui.progressBar.setMinimum(0)
        #ui.progressBar.setFormat("")


# TODO: use iterator?
def pullSettings():
    ui.ExpTimeSpinBox.setValue(fimsettings.parameters['Exposure Time'])
    # if ui.FpsEnableChkBx.isChecked():
    camera.baslerace.setCamAttr('AcquisitionFrameRateEnable', 1)
    ui.FpsDSpinBox.setValue(fimsettings.parameters['Frame Rate'])
    #camera.baslerace.setCamAttr('AcquisitionFrameRateEnable', 0)
    ui.GammaDSpinBox.setValue(fimsettings.parameters['Gamma Correction'])
    ui.GainDSpinBox.setValue(fimsettings.parameters['Gain'])
    ui.BlacklvlDSpinBox.setValue(fimsettings.parameters['Black Level'])
    ui.CutoffSpinBox.setValue(fimsettings.parameters['Cutoff Threshold'])
    ui.CutoffChkBx.setChecked(fimsettings.parameters['Cutoff'])
    ui.StretchHistoDSpinBox.setValue(fimsettings.parameters['Histogram Stretch Factor'])
    ui.StretchHistoChkBx.setChecked(fimsettings.parameters['Stretch Histogram'])
    ui.BgChkBx.setChecked(fimsettings.parameters['Background Subtraction'])
    ui.RecDurTEdit.setTime(QTime.fromString(fimsettings.parameters['Recording Duration']))
    ui.FramesModuloSpinBox.setValue(fimsettings.settings['Extract every n-th Frame'])
    ui.BgSpinBox.setValue(fimsettings.settings['Background Frames to average'])
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
    recordingcam.containerformat = fimsettings.settings['Video Container Format']
    recordingcam.fpath = fimsettings.settings['Recording Directory']
    disposablecam.fpath = fimsettings.settings['Snapshot Directory']
    disposablecam.fileformat = fimsettings.settings['Single Image Format']
    extractcam.fileformat = fimsettings.settings['Single Image Format']
    camera.baslerace.fpath = fimsettings.settings['Configuration Directory']
    camera.baslerace.fname = fimsettings.settings['Default Camera Parameters']


def pushSettings(fpath="", fname="settings.json", onlyparameters=False):
    fimsettings.parameters['Exposure Time'] = ui.ExpTimeSpinBox.value()
    # if ui.FpsEnableChkBx.isChecked():
    fimsettings.parameters['Frame Rate'] = ui.FpsDSpinBox.value()
    fimsettings.parameters['Gamma Correction'] = ui.GammaDSpinBox.value()
    fimsettings.parameters['Gain'] = ui.GainDSpinBox.value()
    fimsettings.parameters['Black Level'] = ui.BlacklvlDSpinBox.value()
    fimsettings.parameters['Cutoff Threshold'] = ui.CutoffSpinBox.value()
    fimsettings.parameters['Cutoff'] = ui.CutoffChkBx.isChecked()
    fimsettings.parameters['Stretch Histogram'] = ui.StretchHistoChkBx.isChecked()
    fimsettings.parameters['Histogram Stretch Factor'] = ui.StretchHistoDSpinBox.value()
    fimsettings.parameters['Background Subtraction'] = ui.BgChkBx.isChecked()
    fimsettings.parameters['Recording Duration'] = ui.RecDurTEdit.time().toString()
    fimsettings.parameters['User Data']['Species'] = speciescell.text()
    fimsettings.parameters['User Data']['Strain'] = straincell.text()
    fimsettings.parameters['User Data']['Genotype'] = genotypecell.text()
    fimsettings.parameters['User Data']['Experiment'] = experimentcell.text()
    fimsettings.parameters['User Data']['Test Conditions'] = testcondcell.text()
    fimsettings.parameters['User Data']['More Info'] = moreinfocell.text()
    fimsettings.settings['Extract every n-th Frame'] = ui.FramesModuloSpinBox.value()
    fimsettings.settings['Background Frames to average'] = ui.BgSpinBox.value()

    # temporarily
    fimsettings.saveSettings(fpath, fname, onlyparameters)

# TODO: Better error handling
def openParamFile():
    ui.selectparamfile.setAcceptMode(QFileDialog.AcceptOpen)
    try:
        completepath = ui.selectparamfile.getOpenFileName(ui.centralwidget, 'Open Parameter File',
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
        completepath = ui.selectparamfile.getSaveFileName(ui.centralwidget, 'Save Parameter File',
                                                      fimsettings.settings['Recording Directory'],
                                                      '*.json')[0]
        fpath = os.path.dirname(completepath)
        fname = os.path.basename(completepath)
        fimsettings.saveSettings(fpath, fname, True)
    except Exception as e:
        logger.exception(str(e))


def open_extern(fname="settings.json"):
    # pushSettings() to edit an up-to-date file
    # not quite perfect
    pushSettings()
    if sys.platform == "win32":
        os.startfile(fname)
        # command = ["cmd", "/c", fname, "&& exit"]
    elif sys.platform == "darwin":
        subprocess.Popen(["open", fname])
    else:
        subprocess.Popen(["xdg-open", fname])


def connectSignals():
    # Print messages to statusbar and console
    camera.device_status[str].connect(ui.statusbar.showMessage)
    #camera.device_status[str].connect(print)
    camera.device_name[str].connect(lambda val: ui.camLabel.setText("Preview (" + val + "):"))
    #disposablecam.status[str].connect(print)
    recordingcam.status[str].connect(ui.statusbar.showMessage)
    extractcam.status[str].connect(ui.statusbar.showMessage)

    if settingswatchdog.addPath("settings.json"):

        def reloadSettings():
            fimsettings.loadSettings()
            pullSettings()
            # Apparantly gedit rewrites text files when saving them,
            # causing QFileSystemWatcher stopping to monitor them
            # This re-adds the file after reloading the modified settings.
            # This definitively does not happen on win32,
            # not sure about darwin and other unixoids, though.
            # Season to taste.
            if sys.platform not in ["win32", "darwin"]:
                settingswatchdog.addPath("settings.json")

        settingswatchdog.fileChanged[str].connect(reloadSettings)

    # Handle QActions
    ui.actionSnapshot.triggered.connect(saveSnapshot)
    ui.actionRefresh.triggered.connect(bootstrapCam)
    ui.actionRecord.toggled[bool].connect(recordVideo)
    ui.actionExtract_Frames_from_Video.toggled[bool].connect(extractFrames)
    ui.actionLoad_Parameters.triggered.connect(openParamFile)
    ui.actionSave_Parameters.triggered.connect(writeParamFile)
    ui.actionSettings.triggered.connect(lambda: open_extern())
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
    extractcam.max_frames.connect(ui.progressBar.setMaximum)
    extractcam.timelimit_reached.connect(ui.actionExtract_Frames_from_Video.toggle)
    extractcam.frame_written.connect(lambda: ui.progressBar.setValue(extractcam.framecount))
    extractcam.frame_written.connect(lambda: ui.progressBar.setFormat(str(extractcam.framecount) +
                                                                      '/' +
                                                                      str(extractcam.maxframes)))

    app.aboutToQuit.connect(pcthread.exit)
    pcthread.started.connect(lambda: previewcam.startProcessing(camera.frame_grabbed))
    # Connect widgets to cam classes and SettingsHandler
    # Replace lambda by functools.partial?
    ui.ExpTimeSpinBox.valueChanged[int].connect(
        lambda val: camera.baslerace.setCamAttr(EXPOSURETIME, val)
    )
    ui.ExpTimeSpinBox.valueChanged[int].connect(
        lambda val: fimsettings.parameters.__setitem__('Exposure Time', val)
    )
    # camera.is_grabbing.connect(lambda: ui.statusbar.showMessage("grabbing..."))
    ui.ExpAutoChkBx.toggled[bool].connect(toggleExposureAuto)
    #ui.FpsEnableChkBx.toggled[bool].connect(
    #    lambda val: camera.baslerace.setCamAttr('AcquisitionFrameRateEnable', int(val))
    #)
    ui.BgChkBx.toggled[bool].connect(
        lambda val: setattr(camera.baslerace, 'subtractbg', val)
    )
    ui.CutoffChkBx.toggled[bool].connect(
        lambda val: setattr(camera.baslerace, 'cutoff', val)
    )
    ui.StretchHistoChkBx.toggled[bool].connect(
        lambda val: setattr(camera.baslerace, 'stretchhistogram', val)
    )
    ui.RecalcBgBtn.pressed.connect(
        lambda: camera.baslerace.resetbackground(ui.BgSpinBox.value())
    )
    ui.FpsDSpinBox.valueChanged[float].connect(
        lambda val: camera.baslerace.setCamAttr(ACQUISITIONFRAMERATE, val)
    )
    ui.GammaDSpinBox.valueChanged[float].connect(
        lambda val: camera.baslerace.setCamAttr('Gamma', val)
    )
    ui.GainDSpinBox.valueChanged[float].connect(
        lambda val: camera.baslerace.setCamAttr('Gain', val)
    )
    ui.BlacklvlDSpinBox.valueChanged[float].connect(
        lambda val: camera.baslerace.setCamAttr('BlackLevel', val)
    )
    ui.CutoffSpinBox.valueChanged[int].connect(
        lambda val: setattr(camera.baslerace, 'threshold', val)
    )
    ui.CutoffSpinBox.valueChanged[int].connect(
        lambda val: logger.debug("Cutoff Threshold: " + str(val))
    )
    ui.StretchHistoDSpinBox.valueChanged[float].connect(
        lambda val: setattr(camera.baslerace, 'stretchfactor', val)
    )
    ui.StretchHistoDSpinBox.valueChanged[float].connect(
        lambda val: logger.debug("Histogram Stretch Factor: " + str(val))
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
    # ui.actionSettings.setDisabled(True)
    # ui.actionSettings.setVisible(False)
    ui.menubar.close()

    if camera.baslerace.emulated:
        ui.BlackLevelLbl.setDisabled(True)
        ui.GainLbl.setDisabled(True)
        ui.GammaLbl.setDisabled(True)
        ui.BlacklvlDSpinBox.setDisabled(True)
        ui.GainDSpinBox.setDisabled(True)
        ui.GammaDSpinBox.setDisabled(True)
        ui.ExpAutoChkBx.setDisabled(True)
        global EXPOSURETIME, ACQUISITIONFRAMERATE
        EXPOSURETIME += 'Abs'
        ACQUISITIONFRAMERATE += 'Abs'


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
    window.showMaximized()
    # window.showNormal()
    recordingcam.moveToThread(recthread)
    extractcam.moveToThread(ecthread)

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
