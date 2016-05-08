"""Defines the Dialogue window"""
from PyQt5 import QtGui, QtWidgets
import sys
import os

import editor.dialogue_design as design
import editor.core as core

class DialogueWindow(QtWidgets.QMainWindow, design.Ui_dialogueWindow):

    def __init__(self, parent, dialogue):
        super().__init__(parent)
        self.setupUi(self)
        self.dialogue = dialogue
        self.init_window()

    def init_window(self):
        # Get all info elements
        name_widget = self.findChild(QtWidgets.QLineEdit, "dialogueName")
        dtext_widget = self.findChild(QtWidgets.QLineEdit, "dialogueDText")
        body_widget = self.findChild(QtWidgets.QTextEdit, "dialogueBody")
        chance_widget = self.findChild(QtWidgets.QSpinBox, "dialogueChance")
        fail_widget = self.findChild(QtWidgets.QLineEdit, "dialogueFail")
        choices_widget = self.findChild(QtWidgets.QListWidget, "choiceList")
        actions_widget = self.findChild(QtWidgets.QListWidget, "actionList")
        conditions_widget = self.findChild(
            QtWidgets.QListWidget, "conditionList")

        # Load info
        name_widget.setText(self.dialogue.name)
        dtext_widget.setText(self.dialogue.dtext)
        body_widget.setText(self.dialogue.body)
        chance_widget.setValue(self.dialogue.chance)
        if self.dialogue.fail:
            fail_widget.setText(self.dialogue.fail)
        if self.dialogue.chance == 100:
            fail_widget.setEnabled(False)
        for dialogue in self.dialogue.choices:
            choices_widget.addItem(dialogue)

        # Connect signals