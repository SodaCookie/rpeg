from PyQt5 import QtGui, QtWidgets, QtCore
from engine.game.dungeon.event import Event
from engine.game.dungeon.dialog import Dialogue
from engine.serialization.serialization import deserialize
from editor.core.floor_handler import FloorHandler
from editor.core.dialogue import DialogueWindow

class ScenarioHandler:
    """Class responsible for handling events/scenarios"""
    EVENTS = {} # Storage variable for events
    dialogue_window = None

    def __init__(self, parent):
        self.parent = parent
        self.floor_handler = FloorHandler()
        self.init_scenario()
        self.current_focus = None

    def init_scenario(self):
        self.EVENTS = deserialize("data/scenario.p")

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

        # Load floor types
        for floor in self.floor_handler.floors():
            floor_combo.addItem(floor.title())

        # Load scenarios to list item
        self.event_to_location = {} # map used to find events by name quickly
        for floor_type in self.EVENTS:
            for room_type in self.EVENTS[floor_type]:
                for event in self.EVENTS[floor_type][room_type]:
                    self.event_to_location[event.name] = \
                        (floor_type, room_type, event)
                    list_widget.addItem(event.name)

        layout = self.parent.findChild(QtWidgets.QVBoxLayout, "dialogueLayout")
        self.set_enable_layout(layout, False)

        # Add slot to list signal
        list_widget.currentItemChanged.connect(self.load_event)
        list_widget.currentItemChanged.connect(self.set_dialogue_enable)
        line_edit.textEdited.connect(self.update_event_name)
        dialogue_widget.itemDoubleClicked.connect(self.open_update_dialogue)
        event_button.clicked.connect(self.new_event)
        dialogue_button.clicked.connect(self.open_new_dialogue)
        floor_combo.currentIndexChanged[str].connect(self.update_event_floor)
        room_combo.currentIndexChanged[str].connect(self.update_event_room)

    def event_key_press(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            item_list = self.parent.findChild(
                QtWidgets.QListWidget, "eventList")
            if item_list.selectedItems():
                reponse = QtWidgets.QMessageBox.question(self.parent, "Delete",
                    "Do you want to delete this event?")
                if reponse == QtWidgets.QMessageBox.Yes:
                    if self.BASE_ITEMS.get(self.current_focus.text()):
                        del self.BASE_ITEMS[self.current_focus.text()]
                    elif self.ITEMS.get(self.current_focus.text()):
                        del self.ITEMS[self.current_focus.text()]
                    item_list.takeItem(item_list.currentRow())

    def set_dialogue_enable(self, next, prev):
        if next != None:
            layout = self.parent.findChild(
                QtWidgets.QVBoxLayout, "dialogueLayout")
            self.set_enable_layout(layout, True)

    def load_event(self, item, prev):
        self.current_focus = item
        floor, room, event = self.event_to_location[self.current_focus.text()]
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
        floor, room, event = self.event_to_location[self.current_focus.text()]
        # Delete previous entry
        del self.event_to_location[event.name]
        # Set text on list widget
        self.current_focus.setText(name)
        # Set actual name
        event.name = name
        # Add back to events map
        self.event_to_location[event.name] = (floor, room, event)

    def update_event_floor(self, floor_type):
        floor, room, event = self.event_to_location[self.current_focus.text()]
        self.EVENTS[floor][room].remove(event)
        self.EVENTS[floor_type.lower()][room].append(event)
        self.event_to_location[self.current_focus.text()] = \
            (floor_type.lower(), room, event)

    def update_event_room(self, room_type):
        floor, room, event = self.event_to_location[self.current_focus.text()]
        self.EVENTS[floor][room].remove(event)
        self.EVENTS[floor][room_type.lower()].append(event)
        self.event_to_location[self.current_focus.text()] = \
            (floor, room_type.lower(), event)

    def new_event(self):
        event_name, ok = QtWidgets.QInputDialog.getText(
            self.parent, 'Add New Event...', 'Enter event name:')

        if ok:
            list_widget = self.parent.findChild(
                QtWidgets.QListWidget, "eventList")
            if not list_widget.findItems(event_name, QtCore.Qt.MatchExactly):
                # Create new event
                new_event = Event(event_name)
                self.EVENTS["any"]["event"].append(new_event)
                # Add to required widgets
                self.event_to_location[new_event.name] = \
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

        dialogue_window = DialogueWindow(self.parent, dialogue)
        dialogue_window.setWindowModality(QtCore.Qt.WindowModal)
        dialogue_window.show()

    def create_dialogue(self, dialogue):
        list_widget = self.parent.findChild(
            QtWidgets.QListWidget, "dialogueList")
        floor, room, event = self.event_to_location[self.current_focus.text()]
        event.dialogues[dialogue.name] = dialogue
        list_widget.addItem(dialogue.name)

    def update_dialogue(self, dialogue):
        list_widget = self.parent.findChild(
            QtWidgets.QListWidget, "dialogueList")
        floor, room, event = self.event_to_location[self.current_focus.text()]
        del event.dialogues[list_widget.currentItem().text()]
        event.dialogues[dialogue.name] = dialogue
        list_widget.currentItem().setText(dialogue.name)

    def open_update_dialogue(self, item):
        """Creates a new dialogue for the editor."""
        # Create a new empty dialogue
        floor, room, event = self.event_to_location[self.current_focus.text()]
        dialogue = event.dialogues[item.text()]

        dialogue_window = DialogueWindow(self.parent, dialogue)
        dialogue_window.setWindowModality(QtCore.Qt.WindowModal)
        dialogue_window.show()

    def set_enable_layout(self, layout, enable):
        """Disables or enables all children in the dialogueLayout"""
        for i in range(layout.count()):
            if isinstance(layout.itemAt(i), QtWidgets.QLayout):
                self.set_enable_layout(layout.itemAt(i), enable)
            else:
                if hasattr(layout.itemAt(i).widget(), "setEnabled"):
                    layout.itemAt(i).widget().setEnabled(enable)