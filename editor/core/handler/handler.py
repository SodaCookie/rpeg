"""Defines the Handler interface"""
from PyQt5 import QtWidgets, QtCore

class Handler(object):

    def __init__(self, parent):
        """Base interface for Handlers to extend to interact with the
        Qt Window."""
        self.focus = None
        self.parent = parent
        self.setup()

    def setup(self):
        """Override. Called whenever class is initiated. Use to hook up
        signals and slots as well as loading data."""
        pass

    def set_focus(self, focus, prev=None):
        """Set focus and call change_focus"""
        self.focus = focus
        self.change_focus(self.focus)

    def change_focus(self, focus):
        """Override. Called whenever focus has changed. Use to load in
        specific data about an object."""
        pass

    def set_enable_layout(self, layout, enable):
        """Convenience function. Disables or enables all children in a
        given layout"""
        for i in range(layout.count()):
            if isinstance(layout.itemAt(i), QtWidgets.QLayout):
                self.set_enable_layout(layout.itemAt(i), enable)
            else:
                if hasattr(layout.itemAt(i).widget(), "setEnabled"):
                    layout.itemAt(i).widget().setEnabled(enable)

    def delete_press_generator(self, obj_type, widget_list, func):
        """Generates an on_delete function that executes a given function when
        delete is pressed."""
        def on_delete(event):
            if event.key() == QtCore.Qt.Key_Delete:
                if widget_list.selectedItems():
                    reponse = QtWidgets.QMessageBox.question(self.parent,
                        "Delete", "Do you want to delete this %s?" % obj_type)
                    if reponse == QtWidgets.QMessageBox.Yes:
                        func(self, widget_list)
        return on_delete