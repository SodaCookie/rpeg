"""Defines the Handler interface"""

class Handler(object):

    def __init__(self, parent):
        """Base interface for Handlers to extend to interact with the
        Qt Window."""
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

