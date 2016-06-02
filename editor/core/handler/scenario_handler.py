from PyQt5 import QtGui, QtWidgets, QtCore

from editor.core.handler.handler import Handler
from engine.game.dungeon.event import Event
from engine.game.dungeon.dialog import Dialogue
from engine.serialization.scenario import EventDataManager
from engine.serialization.floor import FloorDataManager
from editor.core.prompt.dialogue_prompt import DialoguePrompt

class ScenarioHandler(Handler):
    """Class responsible for handling events/scenarios"""
    dialogue_window = None

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        self.floor_dm = FloorDataManager()
        self.event_dm = EventDataManager()

        list_widget = self.parent.findChild(QtWidgets.QListWidget, "eventList")
        line_edit = self.parent.findChild(QtWidgets.QLineEdit, "eventName")
        floor_combo = self.parent.findChild(
            QtWidgets.QComboBox, "eventFloorType")
        room_combo = self.parent.findChild(
            QtWidgets.QComboBox, "eventRoomType")
        event_button = self.parent.findChild(QtWidgets.QPushButton, "newEvent")
        dialogue_button = self.parent.findChild(
            QtWidgets.QPushButton, "newDialogue")
        dialogue_widget = self.parent.findChild(
            QtWidgets.QListWidget, "dialogueList")

        self.load_floors()

        # Load scenarios to list item
        self.event_to_location = {} # map used to find events by name quickly
        for floor_type in self.event_dm.events():
            for room_type in self.event_dm.get()[floor_type]:
                for event in self.event_dm.get()[floor_type][room_type]:
                    self.event_to_location[event.name] = \
                        (floor_type, room_type, event)
                    list_widget.addItem(event.name)

        layout = self.parent.findChild(QtWidgets.QVBoxLayout, "dialogueLayout")
        self.set_enable_layout(layout, False)

        # Add key press event
        list_widget.keyPressEvent = self.delete_press_generator(
            "event", list_widget, self.delete_event)

        # Add slot to list signal
        list_widget.currentItemChanged.connect(self.set_focus)
        list_widget.currentItemChanged.connect(self.set_dialogue_enable)
        line_edit.textEdited.connect(self.update_event_name)
        dialogue_widget.itemDoubleClicked.connect(self.open_update_dialogue)
        event_button.clicked.connect(self.new_event)
        dialogue_button.clicked.connect(self.open_new_dialogue)
        floor_combo.currentIndexChanged[str].connect(self.update_event_floor)
        room_combo.currentIndexChanged[str].connect(self.update_event_room)

    @staticmethod
    def delete_event(self, widget_list):
        floor, room, event = self.event_to_location[self.focus.text()]
        self.event_dm.delete_event(event.name, floor, room)
        widget_list.takeItem(widget_list.currentRow())

    def set_dialogue_enable(self, next, prev):
        if next != None:
            layout = self.parent.findChild(
                QtWidgets.QVBoxLayout, "dialogueLayout")
            self.set_enable_layout(layout, True)

    def change_focus(self, item):
        self.focus = item
        floor, room, event = self.event_to_location[self.focus.text()]
        # Set Line Edit
        line_edit = self.parent.findChild(QtWidgets.QLineEdit, "eventName")
        line_edit.setText(event.name)
        # Set Floor type
        combo_box = self.parent.findChild(
            QtWidgets.QComboBox, "eventFloorType")
        combo_box.setCurrentIndex(combo_box.findText(floor.title()))
        # Set Room type
        combo_box = self.parent.findChild(
            QtWidgets.QComboBox, "eventRoomType")
        combo_box.setCurrentIndex(combo_box.findText(room.title()))
        # Load dialogues
        list_widget = self.parent.findChild(
            QtWidgets.QListWidget, "dialogueList")
        list_widget.clear()
        for name in event.dialogues:
            list_widget.addItem(name)

    def update_event_name(self, name):
        floor, room, event = self.event_to_location[self.focus.text()]
        # Delete previous entry
        del self.event_to_location[event.name]
        # Set text on list widget
        self.focus.setText(name)
        # Set actual name
        self.event_dm.update_event_name(self.focus.text(), floor, room, name)
        # Add back to events map
        self.event_to_location[name] = (floor, room, event)

    def update_event_floor(self, floor_type):
        floor, room, event = self.event_to_location[self.focus.text()]
        self.event_dm.update_event_floor(event.name, floor, room,
            floor_type.lower())
        self.event_to_location[self.focus.text()] = \
            (floor_type.lower(), room, event)

    def update_event_room(self, room_type):
        floor, room, event = self.event_to_location[self.focus.text()]
        self.event_dm.update_event_room(event.name, floor, room,
            room_type.lower())
        self.event_to_location[self.focus.text()] = \
            (floor, room_type.lower(), event)

    def new_event(self):
        event_name, ok = QtWidgets.QInputDialog.getText(
            self.parent, 'Add New Event...', 'Enter event name:')

        if ok:
            list_widget = self.parent.findChild(
                QtWidgets.QListWidget, "eventList")
            if not list_widget.findItems(event_name, QtCore.Qt.MatchExactly):
                # Create new event
                new_event = self.event_dm.new_event(event_name, "any", "event")
                # Add to required widgets
                self.event_to_location[event_name] = \
                    ("any", "event", new_event)
                list_widget.addItem(event_name)
                # The last added
                list_widget.setCurrentRow(list_widget.count()-1)
            else:
                QtWidgets.QMessageBox.warning(
                    self.parent,
                    "Error",
                    "Event name '%s' already exists." % event_name)

    def open_new_dialogue(self):
        """Creates a new dialogue for the editor."""
        # Create a new empty dialogue
        dialogue = Dialogue("", "", "")

        dialogue_window = DialoguePrompt(self.parent, dialogue)
        dialogue_window.setWindowModality(QtCore.Qt.WindowModal)
        dialogue_window.show()

    def create_dialogue(self, dialogue):
        list_widget = self.parent.findChild(
            QtWidgets.QListWidget, "dialogueList")
        floor, room, event = self.event_to_location[self.focus.text()]
        event.dialogues[dialogue.name] = dialogue
        list_widget.addItem(dialogue.name)

    def update_dialogue(self, dialogue):
        list_widget = self.parent.findChild(
            QtWidgets.QListWidget, "dialogueList")
        floor, room, event = self.event_to_location[self.focus.text()]
        self.event_dm.delete_dialogue(event.name, floor, room)
        self.event_dm.add_dialogue(event.name, floor, room, dialogue)
        list_widget.currentItem().setText(dialogue.name)

    def open_update_dialogue(self, item):
        """Creates a new dialogue for the editor."""
        # Create a new empty dialogue
        floor, room, event = self.event_to_location[self.focus.text()]
        dialogue = event.dialogues[item.text()]

        dialogue_window = DialoguePrompt(self.parent, dialogue)
        dialogue_window.setWindowModality(QtCore.Qt.WindowModal)
        dialogue_window.show()

    def load_floors(self):
        floor_combo = self.parent.findChild(
            QtWidgets.QComboBox, "eventFloorType")
        # Load floor types
        floor_combo.clear()
        for floor in self.floor_dm.floors():
            floor_combo.addItem(floor.title())