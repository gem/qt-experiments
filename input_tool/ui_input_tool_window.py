# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_input_tool_window.ui'
#
# Created: Thu Sep 26 15:30:56 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_InputToolWindow(object):
    def setupUi(self, InputToolWindow):
        InputToolWindow.setObjectName(_fromUtf8("InputToolWindow"))
        InputToolWindow.resize(1011, 863)
        self.centralwidget = QtGui.QWidget(InputToolWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabwidget = QtGui.QTabWidget(self.centralwidget)
        self.tabwidget.setObjectName(_fromUtf8("tabwidget"))
        self.exposureModel = QtGui.QWidget()
        self.exposureModel.setObjectName(_fromUtf8("exposureModel"))
        self.tabwidget.addTab(self.exposureModel, _fromUtf8(""))
        self.vulnerabilityModel = QtGui.QWidget()
        self.vulnerabilityModel.setMinimumSize(QtCore.QSize(947, 718))
        self.vulnerabilityModel.setObjectName(_fromUtf8("vulnerabilityModel"))
        self.verticalLayout = QtGui.QVBoxLayout(self.vulnerabilityModel)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.fileNameLbl = QtGui.QLabel(self.vulnerabilityModel)
        self.fileNameLbl.setObjectName(_fromUtf8("fileNameLbl"))
        self.verticalLayout.addWidget(self.fileNameLbl)
        self.vSetsTbl = QtGui.QTableWidget(self.vulnerabilityModel)
        self.vSetsTbl.setAlternatingRowColors(True)
        self.vSetsTbl.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.vSetsTbl.setObjectName(_fromUtf8("vSetsTbl"))
        self.vSetsTbl.setColumnCount(4)
        self.vSetsTbl.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.vSetsTbl.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.vSetsTbl.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.vSetsTbl.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.vSetsTbl.setHorizontalHeaderItem(3, item)
        self.vSetsTbl.horizontalHeader().setDefaultSectionSize(120)
        self.vSetsTbl.horizontalHeader().setSortIndicatorShown(False)
        self.vSetsTbl.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.vSetsTbl)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.vSetsAddBtn = QtGui.QPushButton(self.vulnerabilityModel)
        self.vSetsAddBtn.setObjectName(_fromUtf8("vSetsAddBtn"))
        self.horizontalLayout_3.addWidget(self.vSetsAddBtn)
        self.vSetsDelBtn = QtGui.QPushButton(self.vulnerabilityModel)
        self.vSetsDelBtn.setObjectName(_fromUtf8("vSetsDelBtn"))
        self.horizontalLayout_3.addWidget(self.vSetsDelBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.vFnTbl = QtGui.QTableWidget(self.vulnerabilityModel)
        self.vFnTbl.setAlternatingRowColors(True)
        self.vFnTbl.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.vFnTbl.setObjectName(_fromUtf8("vFnTbl"))
        self.vFnTbl.setColumnCount(2)
        self.vFnTbl.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.vFnTbl.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.vFnTbl.setHorizontalHeaderItem(1, item)
        self.vFnTbl.horizontalHeader().setSortIndicatorShown(False)
        self.vFnTbl.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_2.addWidget(self.vFnTbl)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.vFnAddBtn = QtGui.QPushButton(self.vulnerabilityModel)
        self.vFnAddBtn.setObjectName(_fromUtf8("vFnAddBtn"))
        self.horizontalLayout_2.addWidget(self.vFnAddBtn)
        self.vFnDelBtn = QtGui.QPushButton(self.vulnerabilityModel)
        self.vFnDelBtn.setObjectName(_fromUtf8("vFnDelBtn"))
        self.horizontalLayout_2.addWidget(self.vFnDelBtn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.imlsTbl = QtGui.QTableWidget(self.vulnerabilityModel)
        self.imlsTbl.setAlternatingRowColors(True)
        self.imlsTbl.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.imlsTbl.setObjectName(_fromUtf8("imlsTbl"))
        self.imlsTbl.setColumnCount(3)
        self.imlsTbl.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.imlsTbl.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.imlsTbl.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.imlsTbl.setHorizontalHeaderItem(2, item)
        self.imlsTbl.horizontalHeader().setSortIndicatorShown(False)
        self.imlsTbl.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_3.addWidget(self.imlsTbl)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.imlsAddBtn = QtGui.QPushButton(self.vulnerabilityModel)
        self.imlsAddBtn.setObjectName(_fromUtf8("imlsAddBtn"))
        self.horizontalLayout_5.addWidget(self.imlsAddBtn)
        self.imlsDelBtn = QtGui.QPushButton(self.vulnerabilityModel)
        self.imlsDelBtn.setObjectName(_fromUtf8("imlsDelBtn"))
        self.horizontalLayout_5.addWidget(self.imlsDelBtn)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tabwidget.addTab(self.vulnerabilityModel, _fromUtf8(""))
        self.fragilityModel = QtGui.QWidget()
        self.fragilityModel.setObjectName(_fromUtf8("fragilityModel"))
        self.tabwidget.addTab(self.fragilityModel, _fromUtf8(""))
        self.siteModel = QtGui.QWidget()
        self.siteModel.setObjectName(_fromUtf8("siteModel"))
        self.tabwidget.addTab(self.siteModel, _fromUtf8(""))
        self.ruptureModel = QtGui.QWidget()
        self.ruptureModel.setObjectName(_fromUtf8("ruptureModel"))
        self.tabwidget.addTab(self.ruptureModel, _fromUtf8(""))
        self.config = QtGui.QWidget()
        self.config.setObjectName(_fromUtf8("config"))
        self.tabwidget.addTab(self.config, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabwidget, 1, 0, 1, 1)
        InputToolWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(InputToolWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1011, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        InputToolWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(InputToolWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        InputToolWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(InputToolWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        InputToolWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionOpen = QtGui.QAction(InputToolWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionSave = QtGui.QAction(InputToolWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionCopy = QtGui.QAction(InputToolWindow)
        self.actionCopy.setObjectName(_fromUtf8("actionCopy"))
        self.actionPaste = QtGui.QAction(InputToolWindow)
        self.actionPaste.setObjectName(_fromUtf8("actionPaste"))
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionCopy)
        self.menuFile.addAction(self.actionPaste)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(InputToolWindow)
        self.tabwidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(InputToolWindow)

    def retranslateUi(self, InputToolWindow):
        InputToolWindow.setWindowTitle(QtGui.QApplication.translate("InputToolWindow", "GEM input tool", None, QtGui.QApplication.UnicodeUTF8))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.exposureModel), QtGui.QApplication.translate("InputToolWindow", "Exposure Model", None, QtGui.QApplication.UnicodeUTF8))
        self.fileNameLbl.setText(QtGui.QApplication.translate("InputToolWindow", "<input filename>", None, QtGui.QApplication.UnicodeUTF8))
        self.vSetsTbl.setToolTip(QtGui.QApplication.translate("InputToolWindow", "<html><head/><body><p>Intensity Measure Type</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.vSetsTbl.setSortingEnabled(False)
        item = self.vSetsTbl.horizontalHeaderItem(0)
        item.setText(QtGui.QApplication.translate("InputToolWindow", "Set ID", None, QtGui.QApplication.UnicodeUTF8))
        item = self.vSetsTbl.horizontalHeaderItem(1)
        item.setText(QtGui.QApplication.translate("InputToolWindow", "Asset Category", None, QtGui.QApplication.UnicodeUTF8))
        item = self.vSetsTbl.horizontalHeaderItem(2)
        item.setText(QtGui.QApplication.translate("InputToolWindow", "Loss Category", None, QtGui.QApplication.UnicodeUTF8))
        item = self.vSetsTbl.horizontalHeaderItem(3)
        item.setText(QtGui.QApplication.translate("InputToolWindow", "IMT", None, QtGui.QApplication.UnicodeUTF8))
        self.vSetsAddBtn.setText(QtGui.QApplication.translate("InputToolWindow", "Add Row", None, QtGui.QApplication.UnicodeUTF8))
        self.vSetsDelBtn.setText(QtGui.QApplication.translate("InputToolWindow", "Delete Rows", None, QtGui.QApplication.UnicodeUTF8))
        self.vFnTbl.setSortingEnabled(False)
        item = self.vFnTbl.horizontalHeaderItem(0)
        item.setText(QtGui.QApplication.translate("InputToolWindow", "Fn ID", None, QtGui.QApplication.UnicodeUTF8))
        item = self.vFnTbl.horizontalHeaderItem(1)
        item.setText(QtGui.QApplication.translate("InputToolWindow", "Prob Dist", None, QtGui.QApplication.UnicodeUTF8))
        self.vFnAddBtn.setText(QtGui.QApplication.translate("InputToolWindow", "Add Row", None, QtGui.QApplication.UnicodeUTF8))
        self.vFnDelBtn.setText(QtGui.QApplication.translate("InputToolWindow", "Delete Rows", None, QtGui.QApplication.UnicodeUTF8))
        self.imlsTbl.setSortingEnabled(False)
        item = self.imlsTbl.horizontalHeaderItem(0)
        item.setText(QtGui.QApplication.translate("InputToolWindow", "IML", None, QtGui.QApplication.UnicodeUTF8))
        item = self.imlsTbl.horizontalHeaderItem(1)
        item.setText(QtGui.QApplication.translate("InputToolWindow", "Loss Ratio", None, QtGui.QApplication.UnicodeUTF8))
        item = self.imlsTbl.horizontalHeaderItem(2)
        item.setText(QtGui.QApplication.translate("InputToolWindow", "Coeff Variation", None, QtGui.QApplication.UnicodeUTF8))
        self.imlsAddBtn.setText(QtGui.QApplication.translate("InputToolWindow", "Add Row", None, QtGui.QApplication.UnicodeUTF8))
        self.imlsDelBtn.setText(QtGui.QApplication.translate("InputToolWindow", "Delete Rows", None, QtGui.QApplication.UnicodeUTF8))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.vulnerabilityModel), QtGui.QApplication.translate("InputToolWindow", "Vulnerability Functions", None, QtGui.QApplication.UnicodeUTF8))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.fragilityModel), QtGui.QApplication.translate("InputToolWindow", "Fragility Functions", None, QtGui.QApplication.UnicodeUTF8))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.siteModel), QtGui.QApplication.translate("InputToolWindow", "Site Model", None, QtGui.QApplication.UnicodeUTF8))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.ruptureModel), QtGui.QApplication.translate("InputToolWindow", "Rupture Model", None, QtGui.QApplication.UnicodeUTF8))
        self.tabwidget.setTabText(self.tabwidget.indexOf(self.config), QtGui.QApplication.translate("InputToolWindow", "Config File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("InputToolWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("InputToolWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("InputToolWindow", "&Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setShortcut(QtGui.QApplication.translate("InputToolWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("InputToolWindow", "&Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setShortcut(QtGui.QApplication.translate("InputToolWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setText(QtGui.QApplication.translate("InputToolWindow", "&Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setShortcut(QtGui.QApplication.translate("InputToolWindow", "Ctrl+C", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setText(QtGui.QApplication.translate("InputToolWindow", "&Paste", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setShortcut(QtGui.QApplication.translate("InputToolWindow", "Ctrl+V", None, QtGui.QApplication.UnicodeUTF8))

