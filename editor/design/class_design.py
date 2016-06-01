# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Eric\Documents\GitHub\RPG-Game\editor\scripts/../ui\class.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow.resize(292, 218)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(100, 0))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.classCombo = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.classCombo.sizePolicy().hasHeightForWidth())
        self.classCombo.setSizePolicy(sizePolicy)
        self.classCombo.setObjectName("classCombo")
        self.horizontalLayout.addWidget(self.classCombo)
        self.horizontalLayout.setStretch(1, 2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.attrTable = QtWidgets.QTableWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.attrTable.sizePolicy().hasHeightForWidth())
        self.attrTable.setSizePolicy(sizePolicy)
        self.attrTable.setObjectName("attrTable")
        self.attrTable.setColumnCount(2)
        self.attrTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.attrTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.attrTable.setHorizontalHeaderItem(1, item)
        self.attrTable.horizontalHeader().setStretchLastSection(True)
        self.attrTable.verticalHeader().setVisible(True)
        self.verticalLayout.addWidget(self.attrTable)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.okayButton = QtWidgets.QPushButton(self.centralwidget)
        self.okayButton.setObjectName("okayButton")
        self.horizontalLayout_2.addWidget(self.okayButton)
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_2.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "New Class"))
        self.label.setText(_translate("MainWindow", "Class"))
        item = self.attrTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Parameter"))
        item = self.attrTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Value"))
        self.okayButton.setText(_translate("MainWindow", "OK"))
        self.cancelButton.setText(_translate("MainWindow", "Cancel"))

