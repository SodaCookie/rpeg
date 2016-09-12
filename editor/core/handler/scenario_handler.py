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

        events_widget = self.parent.findChild(QtWidgets.QTreeWidget,
            "eventList")
        line_edit = self.parent.findChild(QtWidgets.QLineEdit, "eventName")
        event_button = self.parent.findChild(QtWidgets.QPushButton, "newEvent")
        dialogue_button = self.parent.findChild(
            QtWidgets.QPushButton, "newDialogue")
        dialogue_widget = self.parent.findChild(
            QtWidgets.QListWidget, "dialogueList")

        # Load scenarios to event tree
        events = self.event_dm.events()
        style = QtWidgets.QCommonStyle()
        floor_icon = style.standardIcon(QtWidgets.QStyle.SP_DirHomeIcon)
        room_icon = style.standardIcon(QtWidgets.QStyle.SP_DirIcon)
        for floor_type in events:
            # Create a floor tab
            floor_item = QtWidgets.QTreeWidgetItem([floor_type.title()])
            floor_item.setIcon(0, floor_icon)
            for room_type in events[floor_type]:
                # Create an room type tab
                room_item = QtWidgets.QTreeWidgetItem([room_type.title()])
                room_item.setIcon(0, room_icon)
                floor_item.addChild(room_item)
                for event in events[floor_type][room_type]:
                    event_item = QtWidgets.QTreeWidgetItem([event.name])
                    event_item.setData(0, QtCore.Qt.UserRole, event)
                    room_item.addChild(event_item)
            events_widget.addTopLevelItem(floor_item)

        layout = self.parent.findChild(QtWidgets.QVBoxLayout, "dialogueLayout")
        self.set_enable_layout(layout, False)

        # Add key press event
        events_widget.keyPressEvent = self.delete_press_generator(
            "event", events_widget, self.delete_event)
        dialogue_widget.keyPressEvent = self.delete_press_generator(
            "dialogue", dialogue_widget, self.delete_dialogue)

        # Add slot to list signal
        events_widget.currentItemChanged.connect(self.callback_select_event)
        events_widget.currentItemChanged.connect(self.set_dialogue_enable)
        events_widget.itemDoubleClicked.connect(self.modify_event_name)
        events_widget.customContextMenuRequested.connect(
            self.callback_event_context)
        line_edit.textEdited.connect(self.update_event_name)
        dialogue_widget.itemDoubleClicked.connect(self.open_update_dialogue)
        event_button.clicked.connect(self.new_event)
        dialogue_button.clicked.connect(self.open_new_dialogue)

    @staticmethod
    def delete_event(self, widget_list):
        floor, room, event = self._get_item_data(self.focus)
        self.event_dm.delete_event(event.name, floor, room)
        widget_list.takeItem(widget_list.currentRow())

    @staticmethod
    def delete_dialogue(self, widget_list):
        floor, room, event = self._get_item_data(self.focus)
        self.event_dm.delete_dialogue(event.name, floor, room,
            widget_list.item(widget_list.currentRow()).text())
        widget_list.takeItem(widget_list.currentRow())

    def set_dialogue_enable(self, next, prev):
        if next != None:
            layout = self.parent.findChild(
                QtWidgets.QVBoxLayout, "dialogueLayout")
            self.set_enable_layout(layout, True)

    def callback_select_event(self, item):
        self.focus = item
        floor, room, event = self._get_item_data(item)
        if not event:
            return # Do nothing

        # Set Line Edit
        line_edit = self.parent.findChild(QtWidgets.QLineEdit, "eventName")
        line_edit.setText(event.name)

        # Load dialogues
        list_widget = self.parent.findChild(
            QtWidgets.QListWidget, "dialogueList")
        list_widget.clear()
        for name in event.dialogues:
            list_widget.addItem(name)

    def update_event_name(self, name):
        floor, room, event = self._get_item_data(self.focus)
        # Delete previous entry
        del self.event_to_location[event.name]
        # Set actual name
        self.event_dm.update_event_name(self.focus.text(), floor, room, name)
        # Set text on list widget
        self.focus.setText(name)
        # Add back to events map
        self.event_to_location[name] = (floor, room, event)

    def update_event_floor(self, floor_type):
        if self.focus:
            floor, room, event = self._get_item_data(self.focus)
            self.event_dm.update_event_floor(event.name, floor, room,
                floor_type.lower())

    def update_event_room(self, room_type):
        floor, room, event = self._get_item_data(self.focus)
        self.event_dm.update_event_room(event.name, floor, room,
            room_type.lower())

    def modify_event_name(self, item):
        floor, room, event = self._get_item_data(item)
        if event:
            event_name, ok = QtWidgets.QInputDialog.getText(
                self.parent, 'Modify Event Name...', 'Enter event name:',
                text=event.name)
            if ok:
                self.update_event_name(event_name)

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
        floor, room, event = self._get_item_data(self.focus)
        dialogue = Dialogue("", "", "", event)

        dialogue_window = DialoguePrompt(self.parent, dialogue)
        dialogue_window.setWindowModality(QtCore.Qt.WindowModal)
        dialogue_window.show()

    def create_dialogue(self, dialogue):
        list_widget = self.parent.findChild(
            QtWidgets.QListWidget, "dialogueList")
        floor, room, event = self._get_item_data(self.focus)
        event.dialogues[dialogue.name] = dialogue
        list_widget.addItem(dialogue.name)

    def update_dialogue(self, dialogue):
        list_widget = self.parent.findChild(
            QtWidgets.QListWidget, "dialogueList")
        floor, room, event = self._get_item_data(self.focus)
        self.event_dm.delete_dialogue(event.name, floor, room, dialogue.name)
        self.event_dm.add_dialogue(event.name, floor, room, dialogue)
        list_widget.currentItem().setText(dialogue.name)

    def open_update_dialogue(self, item):
        """Creates a new dialogue for the editor."""
        # Create a new empty dialogue
        floor, room, event = self._get_item_data(self.focus)
        dialogue = event.dialogues[item.text()]

        dialogue_window = DialoguePrompt(self.parent, dialogue)
        dialogue_window.setWindowModality(QtCore.Qt.WindowModal)
        dialogue_window.show()

    def callback_event_context(self, point):
        """Creates a context menu for when an event gets clicked on."""
        events_widget = self.parent.findChild(QtWidgets.QTreeWidget,
            "eventList")
        item = events_widget.itemAt(point)
        if item:
            floor, room, event = self._get_item_data(item)

            # Create context menu
            menu = QtWidgets.QMenu()
            # New event
            print(room)
            if room and not event:
                menu.addAction("New Event")

            # Modify
            if event:
                menu.addAction("Modify Event")
                move_floor_menu = menu.addMenu("Modify Floor")
                move_room_menu = menu.addMenu("Modify Room")
                menu.addAction("Delete Event")

                for floor in self.floor_dm.floors():
                    move_floor_menu.addAction(floor.title())

                # Static for now
                move_room_menu.addAction("Entrance")
                move_room_menu.addAction("Event")
                move_room_menu.addAction("Monster")
                move_room_menu.addAction("Exit")

                move_room_menu.triggered.connect(self.callback_room_dispatch)
                move_floor_menu.triggered.connect(self.callback_floor_dispatch)

            menu.triggered.connect(self.callback_event_dispatch)
            menu.exec_(events_widget.mapToGlobal(point))

    def callback_event_dispatch(self, action):
        print(action.text())

    def callback_floor_dispatch(self, action):
        print(action.text())

    def callback_room_dispatch(self, action):
        print(action.text())

    def _get_item_data(self, item):
        """Helper function. Returns the floor, room and event info from
        an item."""
        room = None
        floor = None
        event = item.data(0, QtCore.Qt.UserRole)
        if item:
            if item.parent(): # Is a floor or room
                room = item.parent().text(0).lower()
                if item.parent().parent(): # Is a room
                    floor = item.parent().parent().text(0).lower()
                else:
                    floor = room
                    room = item.text(0).lower()
            else:
                floor = item.text(0).lower()
        return floor, room, event
