# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_fimwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_fimWindow(object):
    def setupUi(self, fimWindow):
        fimWindow.setObjectName("fimWindow")
        fimWindow.resize(636, 456)
        fimWindow.setMinimumSize(QtCore.QSize(636, 456))
        self.centralwidget = QtWidgets.QWidget(fimWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(520, 320))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.previewLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previewLabel.sizePolicy().hasHeightForWidth())
        self.previewLabel.setSizePolicy(sizePolicy)
        self.previewLabel.setObjectName("previewLabel")
        self.gridLayout_2.addWidget(self.previewLabel, 0, 1, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tabMeasurement = QtWidgets.QWidget()
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
        self.UserDataTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.UserDataTable.setAlternatingRowColors(True)
        self.UserDataTable.setObjectName("UserDataTable")
        self.UserDataTable.setColumnCount(2)
        self.UserDataTable.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.UserDataTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.UserDataTable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.UserDataTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.UserDataTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        item.setFont(font)
        self.UserDataTable.setItem(0, 0, item)
        self.UserDataTable.horizontalHeader().setStretchLastSection(True)
        self.UserDataTable.verticalHeader().setVisible(False)
        self.gridLayout_3.addWidget(self.UserDataTable, 1, 0, 1, 2)
        self.tabWidget.addTab(self.tabMeasurement, "")
        self.tabCam = QtWidgets.QWidget()
        self.tabCam.setObjectName("tabCam")
        self.gridLayout = QtWidgets.QGridLayout(self.tabCam)
        self.gridLayout.setObjectName("gridLayout")
        self.ExpTimeSpinBox = QtWidgets.QSpinBox(self.tabCam)
        self.ExpTimeSpinBox.setMinimum(34)
        self.ExpTimeSpinBox.setMaximum(10000000)
        self.ExpTimeSpinBox.setSingleStep(100)
        self.ExpTimeSpinBox.setProperty("value", 3000)
        self.ExpTimeSpinBox.setObjectName("ExpTimeSpinBox")
        self.gridLayout.addWidget(self.ExpTimeSpinBox, 0, 2, 1, 1)
        self.ExposureTimeLabel = QtWidgets.QLabel(self.tabCam)
        self.ExposureTimeLabel.setObjectName("ExposureTimeLabel")
        self.gridLayout.addWidget(self.ExposureTimeLabel, 0, 0, 1, 1)
        self.FpsDSpinBox = QtWidgets.QDoubleSpinBox(self.tabCam)
        self.FpsDSpinBox.setEnabled(False)
        self.FpsDSpinBox.setDecimals(5)
        self.FpsDSpinBox.setMinimum(1.0)
        self.FpsDSpinBox.setMaximum(41.58177)
        self.FpsDSpinBox.setSingleStep(0.5)
        self.FpsDSpinBox.setProperty("value", 41.58177)
        self.FpsDSpinBox.setObjectName("FpsDSpinBox")
        self.gridLayout.addWidget(self.FpsDSpinBox, 2, 2, 1, 1)
        self.FpsEnableChkBx = QtWidgets.QCheckBox(self.tabCam)
        self.FpsEnableChkBx.setObjectName("FpsEnableChkBx")
        self.gridLayout.addWidget(self.FpsEnableChkBx, 2, 0, 1, 1)
        self.ExpAutoChkBx = QtWidgets.QCheckBox(self.tabCam)
        self.ExpAutoChkBx.setObjectName("ExpAutoChkBx")
        self.gridLayout.addWidget(self.ExpAutoChkBx, 1, 2, 1, 1)
        self.tabWidget.addTab(self.tabCam, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 3, 1, QtCore.Qt.AlignTop)
        self.camView = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.camView.sizePolicy().hasHeightForWidth())
        self.camView.setSizePolicy(sizePolicy)
        self.camView.setMinimumSize(QtCore.QSize(400, 400))
        self.camView.setSizeIncrement(QtCore.QSize(1, 1))
        self.camView.setText("")
        self.camView.setObjectName("camView")
        self.gridLayout_2.addWidget(self.camView, 1, 1, 1, 1)
        fimWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(fimWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 636, 18))
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
        self.toolBar.setObjectName("toolBar")
        fimWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionLoad_Parameters = QtWidgets.QAction(fimWindow)
        self.actionLoad_Parameters.setObjectName("actionLoad_Parameters")
        self.actionSave_Parameters = QtWidgets.QAction(fimWindow)
        self.actionSave_Parameters.setObjectName("actionSave_Parameters")
        self.actionRecord = QtWidgets.QAction(fimWindow)
        self.actionRecord.setCheckable(True)
        self.actionRecord.setObjectName("actionRecord")
        self.actionRefresh = QtWidgets.QAction(fimWindow)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionSnapshot = QtWidgets.QAction(fimWindow)
        self.actionSnapshot.setObjectName("actionSnapshot")
        self.menuFile.addAction(self.actionLoad_Parameters)
        self.menuFile.addAction(self.actionSave_Parameters)
        self.menuCamera.addAction(self.actionRecord)
        self.menuCamera.addAction(self.actionRefresh)
        self.menuCamera.addAction(self.actionSnapshot)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuCamera.menuAction())
        self.toolBar.addAction(self.actionLoad_Parameters)
        self.toolBar.addAction(self.actionSave_Parameters)
        self.toolBar.addAction(self.actionRecord)
        self.toolBar.addAction(self.actionRefresh)
        self.toolBar.addAction(self.actionSnapshot)

        self.retranslateUi(fimWindow)
        self.tabWidget.setCurrentIndex(1)
        self.actionSnapshot.triggered.connect(self.statusbar.update)
        self.ExpAutoChkBx.toggled['bool'].connect(self.ExpTimeSpinBox.setDisabled)
        self.FpsEnableChkBx.toggled['bool'].connect(self.FpsDSpinBox.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(fimWindow)

    def retranslateUi(self, fimWindow):
        _translate = QtCore.QCoreApplication.translate
        fimWindow.setWindowTitle(_translate("fimWindow", "FIMrecorder"))
        self.previewLabel.setText(_translate("fimWindow", "Preview"))
        self.RecDurLabel.setText(_translate("fimWindow", "Recording Duration:"))
        self.RecDurTEdit.setToolTip(_translate("fimWindow", "HH:mm:ss.ms"))
        self.RecDurTEdit.setDisplayFormat(_translate("fimWindow", "HH:mm:ss.z"))
        item = self.UserDataTable.horizontalHeaderItem(0)
        item.setText(_translate("fimWindow", "Key"))
        item = self.UserDataTable.horizontalHeaderItem(1)
        item.setText(_translate("fimWindow", "Value"))
        __sortingEnabled = self.UserDataTable.isSortingEnabled()
        self.UserDataTable.setSortingEnabled(False)
        self.UserDataTable.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMeasurement), _translate("fimWindow", "Measurement"))
        self.ExposureTimeLabel.setText(_translate("fimWindow", "Exposure Time [µs]"))
        self.FpsEnableChkBx.setText(_translate("fimWindow", "Frame Rate [fps]"))
        self.ExpAutoChkBx.setText(_translate("fimWindow", "Automatic Exposure"))
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
        self.actionRefresh.setText(_translate("fimWindow", "Refresh"))
        self.actionRefresh.setShortcut(_translate("fimWindow", "F5"))
        self.actionSnapshot.setText(_translate("fimWindow", "Snapshot"))
        self.actionSnapshot.setShortcut(_translate("fimWindow", "Alt+S"))

