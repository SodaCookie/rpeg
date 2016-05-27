"""Defines the main Editor window"""
import sys
import os

import sip
from PyQt5 import QtGui, QtWidgets

import editor.design.editor_design as design
import editor.core as core

class Editor(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.scenario_handler = core.ScenarioHandler(self)
        self.item_handler = core.ItemHandler(self)
        self.move_handler = core.MoveHandler(self)
        self.monster_handler = core.MonsterHandler(self)


def init():
    app = QtWidgets.QApplication(sys.argv)
    form = Editor()
    form.show()
    sip.setdestroyonexit(False) # Fixes a crash bug
    sys.exit(app.exec_())