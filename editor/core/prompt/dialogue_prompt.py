"""Defines the Dialogue window"""
from PyQt5 import QtGui, QtWidgets, QtCore
import sys
import os
from copy import copy

from engine.game.dungeon.dialog import Dialogue
import assets.actions
import assets.conditions

from editor.core.prompt.class_prompt import ClassPrompt
import editor.design.dialogue_design as design

class DialoguePrompt(QtWidgets.QMainWindow, design.Ui_dialogueWindow):

    return_dialogue = QtCore.pyqtSignal(Dialogue, name="returnDialogue")

    def __init__(self, parent, dialogue):
        super().__init__(parent)
        self.setupUi(self)
        self.dialogue = copy(dialogue)
        self.init_window()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

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
        choice_button = self.findChild(QtWidgets.QPushButton, "newChoice")
        action_button = self.findChild(QtWidgets.QPushButton, "newAction")
        condition_button = self.findChild(
            QtWidgets.QPushButton, "newCondition")
        create_button = self.findChild(QtWidgets.QPushButton, "createButton")
        cancel_button = self.findChild(QtWidgets.QPushButton, "cancelButton")

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

        # Load Actions and Conditions
        for action in self.dialogue.actions:
            # Get class name
            actions_widget.addItem(type(action).__name__)

        for condition in self.dialogue.conditions:
            # Get class name
            conditions_widget.addItem(type(condition).__name__)

        # Setting key press events
        actions_widget.keyPressEvent = self.action_key_press
        conditions_widget.keyPressEvent = self.condition_key_press
        choices_widget.keyPressEvent = self.choice_key_press

        # Connect signals
        create_button.clicked.connect(self.on_create_clicked)
        cancel_button.clicked.connect(self.on_cancel_clicked)
        name_widget.textEdited.connect(self.update_dialogue_name)
        fail_widget.textEdited.connect(self.update_dialogue_fail)
        dtext_widget.textEdited.connect(self.update_dialogue_dtext)
        body_widget.textChanged.connect(self.update_dialogue_body)
        choice_button.clicked.connect(self.new_choice)
        chance_widget.valueChanged.connect(self.update_dialogue_chance)
        action_button.clicked.connect(self.new_action)
        condition_button.clicked.connect(self.new_condition)
        parent_handler = self.parentWidget().scenario_handler
        if self.dialogue.name:
            self.return_dialogue.connect(parent_handler.update_dialogue)
        else:
            self.return_dialogue.connect(parent_handler.create_dialogue)

    def new_action(self):
        prompt = ClassPrompt(
            self, assets.actions, assets.actions.Action, self.create_action)
        prompt.show()

    def new_condition(self):
        prompt = ClassPrompt(self, assets.conditions,
            assets.conditions.Condition, self.create_condition)
        prompt.show()

    def action_key_press(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            actions_widget = self.findChild(
                QtWidgets.QListWidget, "actionList")
            if actions_widget.selectedItems():
                reponse = QtWidgets.QMessageBox.question(self, "Delete",
                    "Do you want to delete this action?")
                if reponse == QtWidgets.QMessageBox.Yes:
                    del self.dialogue.actions[actions_widget.currentRow()]
                    actions_widget.takeItem(actions_widget.currentRow())

    def condition_key_press(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            conditions_widget = self.findChild(
                QtWidgets.QListWidget, "conditionList")
            if conditions_widget.selectedItems():
                reponse = QtWidgets.QMessageBox.question(self, "Delete",
                    "Do you want to delete this condition?")
                if reponse == QtWidgets.QMessageBox.Yes:
                    del self.dialogue.conditions[
                        conditions_widget.currentRow()]
                    conditions_widget.takeItem(conditions_widget.currentRow())

    def choice_key_press(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            choices_widget = self.findChild(
                QtWidgets.QListWidget, "choiceList")
            if choices_widget.selectedItems():
                reponse = QtWidgets.QMessageBox.question(self, "Delete",
                    "Do you want to delete this choice?")
                if reponse == QtWidgets.QMessageBox.Yes:
                    del self.dialogue.choices[choices_widget.currentRow()]
                    choices_widget.takeItem(choices_widget.currentRow())

    def new_choice(self):
        choice, ok = QtWidgets.QInputDialog.getText(
            self, 'Add New Choice...', 'Enter choice name:')
        if ok:
            choices_widget = self.findChild(
                QtWidgets.QListWidget, "choiceList")
            if not choices_widget.findItems(choice, QtCore.Qt.MatchExactly):
                self.dialogue.choices.append(choice)
                choices_widget.addItem(choice)
            else:
                QtWidgets.QMessageBox.warning(
                    self, "Error", "Choice name '%s' already exists." % choice)

    def update_dialogue_chance(self, value):
        fail_widget = self.findChild(QtWidgets.QLineEdit, "dialogueFail")
        if value == 100:
            fail_widget.setEnabled(False)
        else:
            fail_widget.setEnabled(True)
        self.dialogue.chance = value

    def update_dialogue_name(self, name):
        # Simply set the name
        self.dialogue.name = name

    def update_dialogue_fail(self, fail):
        # Simply set the name
        self.dialogue.fail = fail

    def update_dialogue_dtext(self, dtext):
        self.dialogue.dtext = dtext

    def update_dialogue_body(self):
        body_widget = self.findChild(QtWidgets.QTextEdit, "dialogueBody")
        self.dialogue.body = body_widget.toPlainText()

    def on_create_clicked(self):
        if self.dialogue.name:
            self.return_dialogue.emit(copy(self.dialogue))
            self.close()
        else:
            QtWidgets.QMessageBox.warning(
                self, "Error", "Dialogue must have a name")

    def on_cancel_clicked(self):
        self.close()

    def create_action(self, action):
        self.dialogue.actions.append(action)
        actions_widget = self.findChild(QtWidgets.QListWidget, "actionList")
        actions_widget.addItem(type(action).__name__)

    def create_condition(self, condition):
        self.dialogue.condition.append(condition)
        conditions_widget = self.findChild(
            QtWidgets.QListWidget, "conditionList")
        conditions_widget.addItem(type(condition).__name__)
