"""Defines the Handler interface"""
from PyQt5 import QtWidgets

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