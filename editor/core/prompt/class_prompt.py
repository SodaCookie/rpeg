"""Defines the ClassPrompt window"""
from functools import partial
import sys
import inspect

from PyQt5 import QtGui, QtWidgets, QtCore

import editor.design.class_design as design
import editor.core.prompt.list_prompt
from editor.meta.typecheck import typecheck
from editor.meta.types import *

import assets.moves.components
import assets.attributes
import assets.effects
import assets.actions
import assets.moves.modifiers

from engine.game.move.component import Component
from engine.game.attribute.attribute import Attribute
from engine.game.effect.effect import Effect
from engine.game.dungeon.action import Action
from engine.game.move.modifier import Modifier

class ClassPrompt(QtWidgets.QMainWindow, design.Ui_MainWindow):
    """Class used to help create instances of classes from assets folder"""

    return_dialogue = QtCore.pyqtSignal(object, name="returnDialogue")

    def __init__(self, parent, module, base_class, return_function):
        super().__init__(parent)
        self.setupUi(self)

        # Init instance variables
        self.module = module
        self.classes = dict(inspect.getmembers(module, inspect.isclass))
        self.base_class = base_class
        self.current_cls = None
        self.return_function = return_function
        self.constructor_kwargs = {}

        # Load window
        self.init_window()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def init_window(self):
        class_combo = self.findChild(QtWidgets.QComboBox, "classCombo")
        okay_button = self.findChild(QtWidgets.QPushButton, "okayButton")
        cancel_button = self.findChild(QtWidgets.QPushButton, "cancelButton")
        attr_table = self.findChild(QtWidgets.QTableWidget, "attrTable")

        for name, cls in self.classes.items():
            if issubclass(cls, self.base_class) and cls != self.base_class:
                class_combo.addItem(name)

        # Signals
        class_combo.currentIndexChanged[str].connect(self.selected_class)
        attr_table.cellDoubleClicked.connect(self.modify_parameter)
        okay_button.clicked.connect(self.on_okay_clicked)
        cancel_button.clicked.connect(self.on_cancel_clicked)
        self.return_dialogue.connect(self.return_function)
        self.selected_class(class_combo.currentText())

    def modify_parameter(self, row, column):
        attr_table = self.findChild(QtWidgets.QTableWidget, "attrTable")
        parameter_item = attr_table.item(row, column)
        ptype = parameter_item.data(QtCore.Qt.UserRole)
        if isinstance(ptype, UnknownType):
            code, ok = QtWidgets.QInputDialog.getText(
                self, 'Modify', 'Python code:')
            if ok:
                try:
                    value = eval(code)
                    self.set_parameter(attr_table.item(row, 0).text(),
                        parameter_item, value)
                except:
                    QtWidgets.QMessageBox.warning(
                        self, "Python Error", traceback.format_exc())
        elif isinstance(ptype, ListType):
            prompt = editor.core.prompt.list_prompt.ListPrompt(self, ptype.elemtype, None, partial(self.set_parameter,
                    attr_table.item(row, 0).text(), parameter_item))
            prompt.show()
        elif isinstance(ptype, IntType):
            value, ok = QtWidgets.QInputDialog.getInt(
                self, 'Modify', ' Integer:')
            if ok:
                self.set_parameter(attr_table.item(row, 0).text(),
                    parameter_item, value)
        elif isinstance(ptype, FloatType):
            value, ok = QtWidgets.QInputDialog.getDouble(
                self, 'Modify', ' Float:')
            if ok:
                self.set_parameter(attr_table.item(row, 0).text(),
                    parameter_item, value)
        elif isinstance(ptype, StrType):
            value, ok = QtWidgets.QInputDialog.getText(
                self, 'Modify', ' String:')
            if ok:
                self.set_parameter(attr_table.item(row, 0).text(),
                    parameter_item, value)
        elif isinstance(ptype, LambdaType):
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
        elif isinstance(ptype, ComponentType):
            prompt = ClassPrompt(self, assets.moves.components,
                Component, partial(self.set_parameter,
                    attr_table.item(row, 0).text(), parameter_item))
            prompt.show()
        elif isinstance(ptype, AttributeType):
            prompt = ClassPrompt(self, assets.attributes,
                Attribute, partial(self.set_parameter,
                    attr_table.item(row, 0).text(), parameter_item))
            prompt.show()
        elif isinstance(ptype, EffectType):
            prompt = ClassPrompt(self, assets.effects,
                Effect, partial(self.set_parameter,
                    attr_table.item(row, 0).text(), parameter_item))
            prompt.show()
        elif isinstance(ptype, ModifierType):
            prompt = ClassPrompt(self, assets.moves.modifiers,
                Modifier, partial(self.set_parameter,
                    attr_table.item(row, 0).text(), parameter_item))
            prompt.show()

    def selected_class(self, item):
        # Clear table
        attr_table = self.findChild(QtWidgets.QTableWidget, "attrTable")
        attr_table.setRowCount(0);

        # Assign new attributes
        cls = self.classes[item]
        parameter_types = typecheck(cls)
        self.current_cls = cls
        self.constructor_kwargs = {}
        sig = inspect.signature(cls)
        for parameter in sig.parameters.values():
            attr_table.insertRow(attr_table.rowCount())

            # Set parameter
            parameter_name = QtWidgets.QTableWidgetItem(parameter.name)
            parameter_name.setFlags(QtCore.Qt.NoItemFlags)
            attr_table.setItem(attr_table.rowCount()-1, 0, parameter_name)

            # Set default value
            default = ""
            if parameter.default != inspect.Parameter.empty:
                default = str(parameter.default)
                self.constructor_kwargs[parameter.name] = parameter.default
            parameter_item = QtWidgets.QTableWidgetItem(default)
            parameter_item.setFlags(QtCore.Qt.ItemIsSelectable | \
                QtCore.Qt.ItemIsEnabled)
            parameter_item.setData(QtCore.Qt.UserRole,
                parameter_types[parameter.name])
            attr_table.setItem(attr_table.rowCount()-1, 1, parameter_item)

    def set_parameter(self, parameter, item, value):
        """Helper function to handle setting value to parameters_dict and
        visually updating"""
        self.constructor_kwargs[parameter] = value
        info = repr(value) # Truncate
        info = (info[:30] + '..') if len(info) > 30 else info
        item.setText(info)

    def on_okay_clicked(self):
        attr_table = self.findChild(QtWidgets.QTableWidget, "attrTable")
        try:
            instance = self.current_cls(**self.constructor_kwargs)
        except TypeError:
            print("Parameter error")
        else:
            self.return_dialogue.emit(instance)
            self.close()

    def on_cancel_clicked(self):
        self.close()