# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_fimwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_fimWindow(object):
    def setupUi(self, fimWindow):
        fimWindow.setObjectName("fimWindow")
        fimWindow.resize(900, 600)
        fimWindow.setMinimumSize(QtCore.QSize(900, 600))
        self.centralwidget = QtWidgets.QWidget(fimWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(650, 350))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(False)
        self.progressBar.setMinimumSize(QtCore.QSize(0, 25))
        self.progressBar.setMaximum(1000000)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.progressBar.setFormat("")
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_2.addWidget(self.progressBar, 2, 1, 1, 1)
        self.camLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.camLabel.sizePolicy().hasHeightForWidth())
        self.camLabel.setSizePolicy(sizePolicy)
        self.camLabel.setMinimumSize(QtCore.QSize(0, 10))
        self.camLabel.setObjectName("camLabel")
        self.gridLayout_2.addWidget(self.camLabel, 0, 1, 1, 1)
        self.camWidget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(self.camWidget.sizePolicy().hasHeightForWidth())
        self.camWidget.setSizePolicy(sizePolicy)
        self.camWidget.setMinimumSize(QtCore.QSize(360, 360))
        self.camWidget.setObjectName("camWidget")
        self.gridLayout_2.addWidget(self.camWidget, 1, 1, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(200, 430))
        self.tabWidget.setSizeIncrement(QtCore.QSize(1, 1))
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.ElideLeft)
        self.tabWidget.setObjectName("tabWidget")
        self.tabMeasurement = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.tabMeasurement.sizePolicy().hasHeightForWidth())
        self.tabMeasurement.setSizePolicy(sizePolicy)
        self.tabMeasurement.setMinimumSize(QtCore.QSize(200, 390))
        self.tabMeasurement.setObjectName("tabMeasurement")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tabMeasurement)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.RecDurLabel = QtWidgets.QLabel(self.tabMeasurement)
        self.RecDurLabel.setToolTip("")
        self.RecDurLabel.setObjectName("RecDurLabel")
        self.gridLayout_3.addWidget(self.RecDurLabel, 0, 0, 1, 1)
        self.RecDurTEdit = QtWidgets.QTimeEdit(self.tabMeasurement)
        self.RecDurTEdit.setCurrentSection(QtWidgets.QDateTimeEdit.MinuteSection)
        self.RecDurTEdit.setCurrentSectionIndex(1)
        self.RecDurTEdit.setTime(QtCore.QTime(0, 5, 0))
        self.RecDurTEdit.setObjectName("RecDurTEdit")
        self.gridLayout_3.addWidget(self.RecDurTEdit, 0, 1, 1, 1)
        self.UserDataTable = QtWidgets.QTableWidget(self.tabMeasurement)
        self.UserDataTable.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.UserDataTable.sizePolicy().hasHeightForWidth())
        self.UserDataTable.setSizePolicy(sizePolicy)
        self.UserDataTable.setMinimumSize(QtCore.QSize(0, 300))
        self.UserDataTable.setSizeIncrement(QtCore.QSize(1, 1))
        self.UserDataTable.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.UserDataTable.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.UserDataTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.UserDataTable.setAlternatingRowColors(True)
        self.UserDataTable.setObjectName("UserDataTable")
        self.UserDataTable.setColumnCount(1)
        self.UserDataTable.setRowCount(6)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.UserDataTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.UserDataTable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.UserDataTable.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.UserDataTable.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.UserDataTable.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignTop)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.UserDataTable.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.UserDataTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setItalic(True)
        item.setFont(font)
        self.UserDataTable.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignTop)
        self.UserDataTable.setItem(5, 0, item)
        self.UserDataTable.horizontalHeader().setVisible(False)
        self.UserDataTable.horizontalHeader().setDefaultSectionSize(80)
        self.UserDataTable.horizontalHeader().setStretchLastSection(True)
        self.UserDataTable.verticalHeader().setVisible(True)
        self.UserDataTable.verticalHeader().setDefaultSectionSize(29)
        self.UserDataTable.verticalHeader().setStretchLastSection(True)
        self.gridLayout_3.addWidget(self.UserDataTable, 2, 0, 1, 2)
        self.tabWidget.addTab(self.tabMeasurement, "")
        self.tabCam = QtWidgets.QWidget()
        self.tabCam.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabCam.setObjectName("tabCam")
        self.gridLayout = QtWidgets.QGridLayout(self.tabCam)
        self.gridLayout.setObjectName("gridLayout")
        self.GammaDSpinBox = QtWidgets.QDoubleSpinBox(self.tabCam)
        self.GammaDSpinBox.setEnabled(True)
        self.GammaDSpinBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.GammaDSpinBox.setPrefix("")
        self.GammaDSpinBox.setDecimals(5)
        self.GammaDSpinBox.setMaximum(3.99998)
        self.GammaDSpinBox.setSingleStep(0.1)
        self.GammaDSpinBox.setProperty("value", 1.0)
        self.GammaDSpinBox.setObjectName("GammaDSpinBox")
        self.gridLayout.addWidget(self.GammaDSpinBox, 3, 2, 1, 1)
        self.GainDSpinBox = QtWidgets.QDoubleSpinBox(self.tabCam)
        self.GainDSpinBox.setEnabled(True)
        self.GainDSpinBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.GainDSpinBox.setDecimals(5)
        self.GainDSpinBox.setMaximum(36.0)
        self.GainDSpinBox.setProperty("value", 0.0)
        self.GainDSpinBox.setObjectName("GainDSpinBox")
        self.gridLayout.addWidget(self.GainDSpinBox, 4, 2, 1, 1)
        self.GammaLbl = QtWidgets.QLabel(self.tabCam)
        self.GammaLbl.setObjectName("GammaLbl")
        self.gridLayout.addWidget(self.GammaLbl, 3, 0, 1, 1)
        self.ExpTimeSpinBox = QtWidgets.QSpinBox(self.tabCam)
        self.ExpTimeSpinBox.setMinimum(34)
        self.ExpTimeSpinBox.setMaximum(10000000)
        self.ExpTimeSpinBox.setSingleStep(100)
        self.ExpTimeSpinBox.setProperty("value", 3000)
        self.ExpTimeSpinBox.setObjectName("ExpTimeSpinBox")
        self.gridLayout.addWidget(self.ExpTimeSpinBox, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 10, 0, 1, 1)
        self.RecalcBgBtn = QtWidgets.QPushButton(self.tabCam)
        self.RecalcBgBtn.setEnabled(False)
        self.RecalcBgBtn.setObjectName("RecalcBgBtn")
        self.gridLayout.addWidget(self.RecalcBgBtn, 7, 1, 1, 1)
        self.ExposureTimeLabel = QtWidgets.QLabel(self.tabCam)
        self.ExposureTimeLabel.setObjectName("ExposureTimeLabel")
        self.gridLayout.addWidget(self.ExposureTimeLabel, 0, 0, 1, 1)
        self.FpsDSpinBox = QtWidgets.QDoubleSpinBox(self.tabCam)
        self.FpsDSpinBox.setEnabled(True)
        self.FpsDSpinBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.FpsDSpinBox.setDecimals(5)
        self.FpsDSpinBox.setMinimum(1.0)
        self.FpsDSpinBox.setMaximum(41.58177)
        self.FpsDSpinBox.setSingleStep(0.5)
        self.FpsDSpinBox.setProperty("value", 41.58177)
        self.FpsDSpinBox.setObjectName("FpsDSpinBox")
        self.gridLayout.addWidget(self.FpsDSpinBox, 2, 2, 1, 1)
        self.BlackLevelLbl = QtWidgets.QLabel(self.tabCam)
        self.BlackLevelLbl.setObjectName("BlackLevelLbl")
        self.gridLayout.addWidget(self.BlackLevelLbl, 5, 0, 1, 1)
        self.CutoffChkBx = QtWidgets.QCheckBox(self.tabCam)
        self.CutoffChkBx.setTristate(False)
        self.CutoffChkBx.setObjectName("CutoffChkBx")
        self.gridLayout.addWidget(self.CutoffChkBx, 8, 0, 1, 1)
        self.GainLbl = QtWidgets.QLabel(self.tabCam)
        self.GainLbl.setObjectName("GainLbl")
        self.gridLayout.addWidget(self.GainLbl, 4, 0, 1, 1)
        self.FramesModuloLabel = QtWidgets.QLabel(self.tabCam)
        self.FramesModuloLabel.setWordWrap(True)
        self.FramesModuloLabel.setObjectName("FramesModuloLabel")
        self.gridLayout.addWidget(self.FramesModuloLabel, 11, 0, 1, 1)
        self.BlacklvlDSpinBox = QtWidgets.QDoubleSpinBox(self.tabCam)
        self.BlacklvlDSpinBox.setEnabled(True)
        self.BlacklvlDSpinBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.BlacklvlDSpinBox.setDecimals(5)
        self.BlacklvlDSpinBox.setMaximum(31.9375)
        self.BlacklvlDSpinBox.setProperty("value", 0.0)
        self.BlacklvlDSpinBox.setObjectName("BlacklvlDSpinBox")
        self.gridLayout.addWidget(self.BlacklvlDSpinBox, 5, 2, 1, 1)
        self.ExpAutoChkBx = QtWidgets.QCheckBox(self.tabCam)
        self.ExpAutoChkBx.setObjectName("ExpAutoChkBx")
        self.gridLayout.addWidget(self.ExpAutoChkBx, 1, 2, 1, 1)
        self.FpsLbl = QtWidgets.QLabel(self.tabCam)
        self.FpsLbl.setObjectName("FpsLbl")
        self.gridLayout.addWidget(self.FpsLbl, 2, 0, 1, 1)
        self.CutoffSpinBox = QtWidgets.QSpinBox(self.tabCam)
        self.CutoffSpinBox.setEnabled(False)
        self.CutoffSpinBox.setMaximum(255)
        self.CutoffSpinBox.setObjectName("CutoffSpinBox")
        self.gridLayout.addWidget(self.CutoffSpinBox, 8, 2, 1, 1)
        self.BgSpinBox = QtWidgets.QSpinBox(self.tabCam)
        self.BgSpinBox.setEnabled(False)
        self.BgSpinBox.setMaximum(500)
        self.BgSpinBox.setObjectName("BgSpinBox")
        self.gridLayout.addWidget(self.BgSpinBox, 7, 2, 1, 1)
        self.BgChkBx = QtWidgets.QCheckBox(self.tabCam)
        self.BgChkBx.setObjectName("BgChkBx")
        self.gridLayout.addWidget(self.BgChkBx, 7, 0, 1, 1)
        self.FramesModuloSpinBox = QtWidgets.QSpinBox(self.tabCam)
        self.FramesModuloSpinBox.setMinimum(1)
        self.FramesModuloSpinBox.setMaximum(100000)
        self.FramesModuloSpinBox.setObjectName("FramesModuloSpinBox")
        self.gridLayout.addWidget(self.FramesModuloSpinBox, 11, 2, 1, 1)
        self.StretchHistoChkBx = QtWidgets.QCheckBox(self.tabCam)
        self.StretchHistoChkBx.setObjectName("StretchHistoChkBx")
        self.gridLayout.addWidget(self.StretchHistoChkBx, 9, 0, 1, 1)
        self.StretchHistoDSpinBox = QtWidgets.QDoubleSpinBox(self.tabCam)
        self.StretchHistoDSpinBox.setEnabled(False)
        self.StretchHistoDSpinBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.StretchHistoDSpinBox.setDecimals(5)
        self.StretchHistoDSpinBox.setMaximum(100.0)
        self.StretchHistoDSpinBox.setSingleStep(0.1)
        self.StretchHistoDSpinBox.setObjectName("StretchHistoDSpinBox")
        self.gridLayout.addWidget(self.StretchHistoDSpinBox, 9, 2, 1, 1)
        self.tabWidget.addTab(self.tabCam, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 3, 1)
        fimWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(fimWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 18))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuCamera = QtWidgets.QMenu(self.menubar)
        self.menuCamera.setObjectName("menuCamera")
        fimWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(fimWindow)
        self.statusbar.setObjectName("statusbar")
        fimWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(fimWindow)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolBar.setObjectName("toolBar")
        fimWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionLoad_Parameters = QtWidgets.QAction(fimWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/fa/fa-svgs/solid/folder-open.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/fa/fa-svgs/solid/folder-open.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionLoad_Parameters.setIcon(icon)
        self.actionLoad_Parameters.setObjectName("actionLoad_Parameters")
        self.actionSave_Parameters = QtWidgets.QAction(fimWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/fa/fa-svgs/solid/save.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_Parameters.setIcon(icon1)
        self.actionSave_Parameters.setObjectName("actionSave_Parameters")
        self.actionRecord = QtWidgets.QAction(fimWindow)
        self.actionRecord.setCheckable(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/fa/fa-svgs/solid/video.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":/fa/fa-svgs/solid/video-slash.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionRecord.setIcon(icon2)
        self.actionRecord.setMenuRole(QtWidgets.QAction.NoRole)
        self.actionRecord.setObjectName("actionRecord")
        self.actionRefresh = QtWidgets.QAction(fimWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/fa/fa-svgs/brands/usb.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRefresh.setIcon(icon3)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionSnapshot = QtWidgets.QAction(fimWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/fa/fa-svgs/solid/camera.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSnapshot.setIcon(icon4)
        self.actionSnapshot.setObjectName("actionSnapshot")
        self.actionExtract_Frames_from_Video = QtWidgets.QAction(fimWindow)
        self.actionExtract_Frames_from_Video.setCheckable(True)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/fa/fa-svgs/solid/film.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionExtract_Frames_from_Video.setIcon(icon5)
        self.actionExtract_Frames_from_Video.setObjectName("actionExtract_Frames_from_Video")
        self.actionSettings = QtWidgets.QAction(fimWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/fa/fa-svgs/solid/cogs.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSettings.setIcon(icon6)
        self.actionSettings.setObjectName("actionSettings")
        self.menuFile.addAction(self.actionLoad_Parameters)
        self.menuFile.addAction(self.actionSave_Parameters)
        self.menuCamera.addAction(self.actionRecord)
        self.menuCamera.addAction(self.actionRefresh)
        self.menuCamera.addAction(self.actionSnapshot)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuCamera.menuAction())
        self.toolBar.addAction(self.actionLoad_Parameters)
        self.toolBar.addAction(self.actionSave_Parameters)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRecord)
        self.toolBar.addAction(self.actionRefresh)
        self.toolBar.addAction(self.actionSnapshot)
        self.toolBar.addAction(self.actionExtract_Frames_from_Video)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSettings)

        self.retranslateUi(fimWindow)
        self.tabWidget.setCurrentIndex(0)
        self.actionSnapshot.triggered.connect(self.statusbar.update)
        self.ExpAutoChkBx.toggled['bool'].connect(self.ExpTimeSpinBox.setDisabled)
        self.actionRecord.toggled['bool'].connect(self.actionExtract_Frames_from_Video.setDisabled)
        self.actionExtract_Frames_from_Video.toggled['bool'].connect(self.actionRecord.setDisabled)
        self.CutoffChkBx.toggled['bool'].connect(self.CutoffSpinBox.setEnabled)
        self.BgChkBx.toggled['bool'].connect(self.BgSpinBox.setEnabled)
        self.BgChkBx.toggled['bool'].connect(self.RecalcBgBtn.setEnabled)
        self.StretchHistoChkBx.toggled['bool'].connect(self.StretchHistoDSpinBox.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(fimWindow)

    def retranslateUi(self, fimWindow):
        _translate = QtCore.QCoreApplication.translate
        fimWindow.setWindowTitle(_translate("fimWindow", "FIMrecorder"))
        self.camLabel.setText(_translate("fimWindow", "Preview (no device):"))
        self.RecDurLabel.setText(_translate("fimWindow", "Recording Duration:"))
        self.RecDurTEdit.setToolTip(_translate("fimWindow", "HH:mm:ss.ms"))
        self.RecDurTEdit.setDisplayFormat(_translate("fimWindow", "HH:mm:ss.z"))
        item = self.UserDataTable.verticalHeaderItem(0)
        item.setText(_translate("fimWindow", "Species"))
        item = self.UserDataTable.verticalHeaderItem(1)
        item.setText(_translate("fimWindow", "Strain"))
        item = self.UserDataTable.verticalHeaderItem(2)
        item.setText(_translate("fimWindow", "Genotype  "))
        item = self.UserDataTable.verticalHeaderItem(3)
        item.setText(_translate("fimWindow", "Experiment"))
        item = self.UserDataTable.verticalHeaderItem(4)
        item.setText(_translate("fimWindow", "Test Conditions  "))
        item = self.UserDataTable.verticalHeaderItem(5)
        item.setText(_translate("fimWindow", "More Info"))
        item = self.UserDataTable.horizontalHeaderItem(0)
        item.setText(_translate("fimWindow", "Value"))
        __sortingEnabled = self.UserDataTable.isSortingEnabled()
        self.UserDataTable.setSortingEnabled(False)
        self.UserDataTable.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMeasurement), _translate("fimWindow", "Measurement"))
        self.GammaLbl.setText(_translate("fimWindow", "Gamma Correction"))
        self.RecalcBgBtn.setText(_translate("fimWindow", "Recalculate Background"))
        self.ExposureTimeLabel.setText(_translate("fimWindow", "Exposure Time [µs]"))
        self.BlackLevelLbl.setText(_translate("fimWindow", "Black Level"))
        self.CutoffChkBx.setToolTip(_translate("fimWindow", "This sets all pixel values below the specified threshold to black."))
        self.CutoffChkBx.setText(_translate("fimWindow", "Cutoff Threshold"))
        self.GainLbl.setText(_translate("fimWindow", "Gain [dB]"))
        self.FramesModuloLabel.setToolTip(_translate("fimWindow", "How many frames do you want to include when extracting frames from a video file?"))
        self.FramesModuloLabel.setText(_translate("fimWindow", "Extract every n-th frame from Video:"))
        self.ExpAutoChkBx.setText(_translate("fimWindow", "Automatic Exposure"))
        self.FpsLbl.setText(_translate("fimWindow", "Frame Rate [fps]"))
        self.BgChkBx.setText(_translate("fimWindow", "Subtract Background"))
        self.FramesModuloSpinBox.setToolTip(_translate("fimWindow", "Choosing a value corresponding to the frame rate of your file results in extracting one frame every second of the video."))
        self.StretchHistoChkBx.setToolTip(_translate("fimWindow", "This increases contrast by multiplying frames elementwise with themselves. This can be adjustet with a certain scale factor."))
        self.StretchHistoChkBx.setText(_translate("fimWindow", "Stretch Histogram"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCam), _translate("fimWindow", "Camera"))
        self.menuFile.setTitle(_translate("fimWindow", "File"))
        self.menuCamera.setTitle(_translate("fimWindow", "Camera"))
        self.toolBar.setWindowTitle(_translate("fimWindow", "toolBar"))
        self.actionLoad_Parameters.setText(_translate("fimWindow", "Load Parameters"))
        self.actionLoad_Parameters.setShortcut(_translate("fimWindow", "Ctrl+O"))
        self.actionSave_Parameters.setText(_translate("fimWindow", "Save Parameters"))
        self.actionSave_Parameters.setShortcut(_translate("fimWindow", "Ctrl+S"))
        self.actionRecord.setText(_translate("fimWindow", "Record"))
        self.actionRecord.setShortcut(_translate("fimWindow", "Ctrl+R"))
        self.actionRefresh.setText(_translate("fimWindow", "Find Camera"))
        self.actionRefresh.setShortcut(_translate("fimWindow", "F5"))
        self.actionSnapshot.setText(_translate("fimWindow", "Snapshot"))
        self.actionSnapshot.setShortcut(_translate("fimWindow", "Alt+S"))
        self.actionExtract_Frames_from_Video.setText(_translate("fimWindow", "Extract Frames from Video"))
        self.actionExtract_Frames_from_Video.setToolTip(_translate("fimWindow", "Choose a recorded .avi file to extract .png frames into a subfolder"))
        self.actionSettings.setText(_translate("fimWindow", "Settings"))
        self.actionSettings.setToolTip(_translate("fimWindow", "Open settings file"))

from . import fimui_rc
