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
        self.tabWidget.addTab(self.tabMeasurement, "")
        self.tabCam = QtWidgets.QWidget()
        self.tabCam.setObjectName("tabCam")
        self.tabWidget.addTab(self.tabCam, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 3, 1)
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
        QtCore.QMetaObject.connectSlotsByName(fimWindow)

    def retranslateUi(self, fimWindow):
        _translate = QtCore.QCoreApplication.translate
        fimWindow.setWindowTitle(_translate("fimWindow", "FIMrecorder"))
        self.previewLabel.setText(_translate("fimWindow", "Preview"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMeasurement), _translate("fimWindow", "Measurement"))
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

