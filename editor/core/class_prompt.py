"""Defines the ClassPrompt window"""
from PyQt5 import QtGui, QtWidgets, QtCore
import sys
import inspect

import editor.class_design as design
import editor.core as core

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

        # Load window
        self.init_window()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def init_window(self):
        class_combo = self.findChild(QtWidgets.QComboBox, "classCombo")
        okay_button = self.findChild(QtWidgets.QPushButton, "okayButton")
        cancel_button = self.findChild(QtWidgets.QPushButton, "cancelButton")

        for name, cls in self.classes.items():
            if issubclass(cls, self.base_class) and cls != self.base_class:
                class_combo.addItem(name)

        # Signals
        class_combo.currentIndexChanged[str].connect(self.selected_class)
        okay_button.clicked.connect(self.on_okay_clicked)
        cancel_button.clicked.connect(self.on_cancel_clicked)
        self.return_dialogue.connect(self.return_function)
        self.selected_class(class_combo.currentText())

    def selected_class(self, item):
        # Clear table
        attr_table = self.findChild(QtWidgets.QTableWidget, "attrTable")
        attr_table.setRowCount(0);

        # Assign new attributes
        cls = self.classes[item]
        self.current_cls = cls
        sig = inspect.signature(cls)
        for parameter in sig.parameters.values():
            attr_table.insertRow(attr_table.rowCount())
            # Set parameter
            parameter_item = QtWidgets.QTableWidgetItem(parameter.name)
            parameter_item.setFlags(QtCore.Qt.NoItemFlags)
            attr_table.setItem(attr_table.rowCount()-1, 0, parameter_item)
            # Set default value
            if parameter.default != inspect.Parameter.empty:
                parameter_item = QtWidgets.QTableWidgetItem(
                    repr(parameter.default))
                attr_table.setItem(attr_table.rowCount()-1, 1, parameter_item)

    def on_okay_clicked(self):
        attr_table = self.findChild(QtWidgets.QTableWidget, "attrTable")
        parameters = {}
        for row in range(attr_table.rowCount()):
            name = attr_table.itemAt(row, 0).text()
            value = attr_table.item(row, 1).text()
            parameters[name] = eval(value)
        instance = self.current_cls(**parameters)
        self.return_dialogue.emit(instance)
        self.close()

    def on_cancel_clicked(self):
        self.close()