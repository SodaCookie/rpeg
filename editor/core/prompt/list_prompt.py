"""Defines the ListPrompt window"""
from functools import partial
import sys

from PyQt5 import QtGui, QtWidgets, QtCore

import editor.core.prompt.class_prompt
import editor.design.list_design as design
from editor.meta.types import *

import assets.moves.components
import assets.attributes
import assets.effects
import assets.actions
import assets.moves.modifiers

# Needs a refactor to extend the Handler
from editor.core.handler.handler import Handler
from editor.meta.types import *

from engine.game.move.component import Component
from engine.game.attribute.attribute import Attribute
from engine.game.effect.effect import Effect
from engine.game.dungeon.action import Action
from engine.game.move.modifier import Modifier

class ListPrompt(QtWidgets.QMainWindow, design.Ui_MainWindow):
    """Class used to help create list types"""

    return_dialogue = QtCore.pyqtSignal(object, name="returnDialogue")

    def __init__(self, parent, itype, init_list, return_function):
        super().__init__(parent)
        self.setupUi(self)

        # Init instance variables
        self.itype = itype
        self.return_list = init_list if init_list is not None else []
        self.return_function = return_function

        # Load window
        self.init_window()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.parent = parent # Temp fix for generate_deleter bug

    def init_window(self):
        list_widget = self.findChild(QtWidgets.QListWidget, "listWidget")
        new_button = self.findChild(QtWidgets.QPushButton, "newButton")
        close_button = self.findChild(QtWidgets.QPushButton, "closeButton")

        for item in self.return_list:
            list_widget.addItem(str(item))

        # Set deleter
        self.listWidget.keyPressEvent = Handler.delete_press_generator(
            self, str(self.itype), list_widget, self.delete_value)

        # Signals
        list_widget.itemDoubleClicked.connect(partial(self._dispatch_setter,
            self.modify_value))
        new_button.clicked.connect(partial(self._dispatch_setter,
            self.add_value))
        close_button.clicked.connect(self.on_close_clicked)
        self.return_dialogue.connect(self.return_function)

    @staticmethod
    def delete_value(self, widget_list):
        del self.return_list[widget_list.currentRow()]
        widget_list.takeItem(widget_list.currentRow())

    def add_value(self, value):
        list_widget = self.findChild(QtWidgets.QListWidget, "listWidget")
        list_widget.addItem(str(value))
        self.return_list.append(value)

    def modify_value(self, value):
        list_widget = self.findChild(QtWidgets.QListWidget, "listWidget")
        list_widget.item(list_widget.currentRow()).setText(str(value))
        self.return_list[list_widget.currentRow()] = value

    def _dispatch_setter(self, call_back, item):
        """Helper function to dispatch the proper prompt to construct"""
        if isinstance(self.itype, UnknownType):
            code, ok = QtWidgets.QInputDialog.getText(
                self, 'Modify', 'Python code:')
            if ok:
                try:
                    value = eval(code)
                    call_back(value)
                except:
                    QtWidgets.QMessageBox.warning(
                        self, "Python Error", traceback.format_exc())
        elif isinstance(self.itype, ListType):
            prompt = ListPrompt(self, self.itype.elemtype, None, call_back)
            prompt.show()
        elif isinstance(self.itype, IntType):
            value, ok = QtWidgets.QInputDialog.getInt(
                self, 'Modify', ' Integer:')
            if ok:
                call_back(value)
        elif isinstance(self.itype, FloatType):
            value, ok = QtWidgets.QInputDialog.getDouble(
                self, 'Modify', ' Float:')
            if ok:
                call_back(value)
        elif isinstance(self.itype, StrType):
            value, ok = QtWidgets.QInputDialog.getText(
                self, 'Modify', ' String:')
            if ok:
                call_back(value)
        elif isinstance(self.itype, LambdaType):
            code, ok = QtWidgets.QInputDialog.getText(
                self, 'Modify', 'Python code:')
            if ok:
                try:
                    value = eval(code)
                    self.set_parameter(attr_table.item(row, 0).text(),
                        parameter_item, value)
                except:
                    QtWidgets.QMessageBox.warning(
                        self.parent,
                        "Python Error",
                        traceback.format_exc())
        elif isinstance(self.itype, ComponentType):
            prompt = editor.core.prompt.class_prompt.ClassPrompt(
                self, assets.moves.components, Component, call_back)
            prompt.show()
        elif isinstance(self.itype, AttributeType):
            prompt = editor.core.prompt.class_prompt.ClassPrompt(
                self, assets.attributes, Attribute, call_back)
            prompt.show()
        elif isinstance(self.itype, EffectType):
            prompt = editor.core.prompt.class_prompt.ClassPrompt(
                self, assets.effects, Effect, call_back)
            prompt.show()
        elif isinstance(self.itype, ModifierType):
            prompt = editor.core.prompt.class_prompt.ClassPrompt(
                self, assets.moves.modifiers, Modifier, call_back)
            prompt.show()

    def on_close_clicked(self):
        self.return_dialogue.emit(self.return_list)
        self.close()