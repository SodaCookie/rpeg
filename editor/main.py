"""Defines the main Editor window"""
from PyQt5 import QtGui, QtWidgets
import sys
import os

import editor.design as design
import editor.core as core

class Editor(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.scenario_handler = core.scenario.ScenarioHandler(self)
        self.item_handler = core.item.ItemHandler(self)


def init():
    app = QtWidgets.QApplication(sys.argv)
    form = Editor()
    form.show()
    app.exec_()