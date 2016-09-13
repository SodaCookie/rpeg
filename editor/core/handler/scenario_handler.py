from PyQt5 import QtGui, QtWidgets, QtCore

from editor.core.handler.handler import Handler
from engine.game.dungeon.event import Event
from engine.game.dungeon.dialog import Dialogue
from engine.serialization.scenario import EventDataManager
from engine.serialization.floor import FloorDataManager
from editor.core.prompt.dialogue_prompt import DialoguePrompt
from editor.core.prompt.event_prompt import EventPrompt

class ScenarioHandler(Handler):
    """Class responsible for handling events/scenarios"""

    NEW_EVENT_ACTION = QtWidgets.QAction("New Event", None)
    MODIFY_EVENT_ACTION = QtWidgets.QAction("Modify Event", None)
    DELETE_EVENT_ACTION = QtWidgets.QAction("Delete Event", None)

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        self.floor_dm = FloorDataManager()
        self.event_dm = EventDataManager()

        events_widget = self.parent.findChild(QtWidgets.QTreeWidget,
            "events")
        line_edit = self.parent.findChild(QtWidgets.QLineEdit, "eventName")
        event_button = self.parent.findChild(QtWidgets.QPushButton, "newEvent")
        dialogue_button = self.parent.findChild(
            QtWidgets.QPushButton, "newDialogue")
        dialogue_widget = self.parent.findChild(
            QtWidgets.QTreeWidget, "dialogues")

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
        events_widget.customContextMenuRequested.connect(
            self.callback_event_context)
        line_edit.textEdited.connect(self.update_event_name)
        dialogue_widget.itemDoubleClicked.connect(self.create_dialogue_prompt)
        event_button.clicked.connect(self.create_event_prompt)
        dialogue_button.clicked.connect(self.open_new_dialogue)

    #================== CONTEXT CODE ==================#
    def callback_event_context(self, point):
        """Creates a context menu for when an event gets clicked on."""
        events_widget = self.parent.findChild(QtWidgets.QTreeWidget,
            "events")
        item = events_widget.itemAt(point)
        if item:
            floor, room, event = self._get_item_data(item)

            # Create context menu
            menu = QtWidgets.QMenu("event")
            # New event
            if room and not event:
                menu.addAction(ScenarioHandler.NEW_EVENT_ACTION)

            # Modify
            if event:
                menu.addAction(ScenarioHandler.MODIFY_EVENT_ACTION)
                move_floor_menu = menu.addMenu("Modify Floor")
                move_room_menu = menu.addMenu("Modify Room")
                menu.addAction(ScenarioHandler.DELETE_EVENT_ACTION)

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
        """Callback whenever an event action is executed"""
        if action == ScenarioHandler.NEW_EVENT_ACTION:
            self.create_event_prompt(*self._get_item_data(self.focus))
        elif action == ScenarioHandler.MODIFY_EVENT_ACTION:
            self.create_event_prompt(*self._get_item_data(self.focus), mod=True)
        elif action == ScenarioHandler.DELETE_EVENT_ACTION:
            self.delete_event(self.focus)

    def callback_floor_dispatch(self, action):
        """Callback whenever a scenario is asked to be moved to a new floor"""
        floor, room, event = self._get_item_data(self.focus)
        self.move_event(event, (floor, room), (action.text().lower(), room))

    def callback_room_dispatch(self, action):
        """Callback whenever a scenario is asked to be moved to a new room"""
        floor, room, event = self._get_item_data(self.focus)
        self.move_event(event, (floor, room), (floor, action.text().lower()))

    #================== EVENT CODE ==================#
    def delete_event(self, item):
        """Deletes an event item from our tree and system. Takes the item."""
        floor, room, event = self._get_item_data(item)
        self.event_dm.delete_event(event.name, floor, room)
        index = item.parent().indexOfChild(item)
        item.parent().takeChild(index)

    def move_event(self, event, prev, dest):
        """Moves the event and calls the DataManager"""
        # Unpack prev and dest
        prev_floor, prev_room = prev
        dest_floor, dest_room = dest

        # Pop event_item
        event_item = self.focus.parent().takeChild(
            self.focus.parent().indexOfChild(self.focus))

        # Find parent_item
        parent_item = self._get_room_of_floor(dest_floor, dest_room)
        assert parent_item, "Parent item not found"

        events_widget = self.parent.findChild(QtWidgets.QTreeWidget, "events")

        # Add the item
        parent_item.addChild(event_item)
        events_widget.setCurrentItem(event_item)

        # Update event and item
        self.event_dm.update_event_floor(event.name, prev_floor, prev_room,
            dest_floor)
        self.event_dm.update_event_room(event.name, prev_floor, prev_room,
            dest_room)

    def update_event_name(self, name):
        floor, room, event = self._get_item_data(self.focus)
        # Set actual name
        self.event_dm.update_event_name(self.focus.text(0), floor, room, name)
        # Set text on list widget
        self.focus.setText(0, name)

    def create_event_prompt(self, floor=None, room=None, event=None, mod=False):
        """Creates a new event prompt to either create a new event or
        modify an original one."""
        event_prompt = EventPrompt(self.parent, floor, room, event)

        if event_prompt.exec_():
            events_widget = self.parent.findChild(QtWidgets.QTreeWidget,
                "events")
            settings = event_prompt.settings
            # Create new event
            if not mod:
                if not events_widget.findItems(settings["name"],
                        QtCore.Qt.MatchExactly):
                    # Create new event
                    new_event = self.event_dm.new_event(settings["name"],
                        settings["floor"], settings["room"])

                    # Create tree item
                    event_item = QtWidgets.QTreeWidgetItem([settings["name"]])
                    event_item.setData(0, QtCore.Qt.UserRole, new_event)

                    parent_item = None
                    # Search for floor and room
                    parent_item = self._get_room_of_floor(settings["floor"],
                        settings["room"])
                    assert parent_item, "Parent item not found"

                    parent_item.addChild(event_item)
                    events_widget.setCurrentItem(event_item)
                else:
                    QtWidgets.QMessageBox.warning(
                        self.parent, "Error",
                        "Event name '%s' already exists." % settings["name"])
            # Modify an existing event
            else:
                # Get the event item
                event_item = self.focus.parent().takeChild(
                    self.focus.parent().indexOfChild(self.focus))

                # Pop the event item
                parent_item = self._get_room_of_floor(settings["floor"],
                    settings["room"])
                assert parent_item, "Parent item not found"

                # Add the item
                parent_item.addChild(event_item)
                events_widget.setCurrentItem(event_item)

                # Update event and item
                self.move_event(event, (floor, room),
                               (settings["floor", "room"]))
                self.event_dm.update_event_name(event.name, floor, room,
                                                settings["name"])
                event_item.setText(settings["name"])

    #================== DIALOGUE CODE ==================#
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
        dialogues = self.parent.findChild(QtWidgets.QTreeWidget, "dialogues")

        # Populate tree
        dialogues.clear()
        self._load_dialogue(event, "main", None, set())

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

    def create_dialogue_prompt(self, item):
        """Creates a new dialogue for the editor."""
        # Create a new empty dialogue
        floor, room, event = self._get_item_data(self.focus)
        dialogue = event.dialogues[item.text(0)]

        dialogue_window = DialoguePrompt(self.parent, dialogue)
        dialogue_window.setWindowModality(QtCore.Qt.WindowModal)
        dialogue_window.show()

    #================== HELPER FUNCTIONS ==================#
    def _load_dialogue(self, event, key, parent, visited):
        """Helper function.
        Recursively populate the event tree."""
        visited.add(key)
        cur_dialog = event.dialogues.get(key)
        cur_item = QtWidgets.QTreeWidgetItem([key])
        if not cur_dialog: # Base-case
            cur_item.setForeground(0, QtGui.QBrush(QtGui.QColor("light grey")))
        else:
            # Push a full item to dialogue and find children
            if cur_dialog.choices:
                for child in cur_dialog.choices:
                    if child not in visited:
                        self._load_dialogue(event, child, cur_item, visited)
                    else:
                        # Create a new link
                        link_item = QtWidgets.QTreeWidgetItem([child])
                        link_item.setFlags()
                        link_item.setForeground(0, QtGui.QBrush(
                            QtGui.QColor("light blue")))
                        cur_item.addChild(link_item)
        # Add to item or to the top level
        if parent:
            parent.addChild(cur_item)
            parent.setExpanded(True)
        else:
            self.parent.dialogues.addTopLevelItem(cur_item)
            cur_item.setExpanded(True)

    def _get_room_of_floor(self, floor, room):
        """Helper function that finds the floor/room item."""
        item = None
        events_widget = self.parent.findChild(QtWidgets.QTreeWidget,
            "events")
        # Search for floor and room
        for i in range(events_widget.topLevelItemCount()):
            floor_item = events_widget.topLevelItem(i)
            if floor_item.text(0).lower() == floor:
                for j in range(floor_item.childCount()):
                    room_item = floor_item.child(j)
                    if room_item.text(0).lower() == room:
                        item = room_item
        return item

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
