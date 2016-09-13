# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/ericzhang/Documents/GitHub/rpeg/editor/scripts/../ui/event.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NewEvent(object):
    def setupUi(self, NewEvent):
        NewEvent.setObjectName("NewEvent")
        NewEvent.resize(278, 145)
        self.gridLayout = QtWidgets.QGridLayout(NewEvent)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(NewEvent)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.name = QtWidgets.QLineEdit(NewEvent)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(NewEvent)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.room = QtWidgets.QComboBox(NewEvent)
        self.room.setObjectName("room")
        self.room.addItem("")
        self.room.setItemText(0, "")
        self.gridLayout.addWidget(self.room, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(NewEvent)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.floor = QtWidgets.QComboBox(NewEvent)
        self.floor.setObjectName("floor")
        self.floor.addItem("")
        self.floor.setItemText(0, "")
        self.gridLayout.addWidget(self.floor, 2, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(NewEvent)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)

        self.retranslateUi(NewEvent)
        self.buttonBox.accepted.connect(NewEvent.accept)
        self.buttonBox.rejected.connect(NewEvent.reject)
        QtCore.QMetaObject.connectSlotsByName(NewEvent)

    def retranslateUi(self, NewEvent):
        _translate = QtCore.QCoreApplication.translate
        NewEvent.setWindowTitle(_translate("NewEvent", "Create New Event"))
        self.label.setText(_translate("NewEvent", "Name"))
        self.label_2.setText(_translate("NewEvent", "Room"))
        self.label_3.setText(_translate("NewEvent", "Floor"))

