from PyQt5 import QtGui, QtWidgets
from engine.game.dungeon.event import Event
from engine.serialization.serialization import deserialize

class ScenarioHandler:
    """Class responsible for handling events/scenarios"""
    EVENTS = {} # Storage variable for events

    def __init__(self, parent=None):
        self.parent = parent
        self.init_scenario()
        self.current_focus = None

    def init_scenario(self):
        self.EVENTS = deserialize("data/scenario.p")
        list_widget = self.parent.findChild(QtWidgets.QListWidget, "eventList")
        line_edit = self.parent.findChild(QtWidgets.QLineEdit, "eventName")

        # Add slot to list signal
        list_widget.itemClicked.connect(self.load_event)
        line_edit.textEdited.connect(self.update_event_name)

        # Load scenarios to list item
        self.events_by_name = {} # map used to find events by name quickly
        for floor_type in self.EVENTS:
            for room_type in self.EVENTS[floor_type]:
                for event in self.EVENTS[floor_type][room_type]:
                    self.events_by_name[event.name] = event
                    list_widget.addItem(event.name)

        if list_widget.count() > 0:
            list_widget.setCurrentRow(0)
        else:
            layout = self.parent.findChild(
                QtWidgets.QVBoxLayout, "dialogueLayout")
            layout.setEnabled(False)

    def load_event(self, item):
        self.current_focus = item
        event = self.events_by_name[item.text()]
        line_edit = self.parent.findChild(QtWidgets.QLineEdit, "eventName")
        line_edit.setText(event.name)

    def update_event_name(self, name):
        event = self.events_by_name[self.current_focus.text()]
        # Delete previous entry
        del self.events_by_name[event.name]
        # Set text on list widget
        self.current_focus.setText(name)
        # Set actual name
        event.name = name
        # Add back to events map
        self.events_by_name[event.name] = event

    def new_scenario(self, name):
        return Event(name)
