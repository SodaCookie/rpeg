"""Defines the Dialogue window"""
from PyQt5 import QtGui, QtWidgets, QtCore
import sys

from editor.core.prompt.class_prompt import ClassPrompt
from engine.serialization.floor import FloorDataManager
import editor.design.event_design as design

class EventPrompt(QtWidgets.QDialog, design.Ui_NewEvent):

    def __init__(self, parent, floor=None, room=None, event=None):
        super().__init__()
        self.setupUi(self)
        self.floor_dm = FloorDataManager()
        self.settings = {
            "name" : event.name if event else "",
            "room" : room if room else "",
            "floor" : floor if floor else ""
        }

        # Floors
        for floor in self.floor_dm.floors():
            self.floor.addItem(floor.title())

        # Room
        self.room.addItem("Entrance")
        self.room.addItem("Event")
        self.room.addItem("Monster")
        self.room.addItem("Exit")

        # Connection to signals
        self.name.textEdited.connect(self.callback_name_textEdited)
        self.room.currentIndexChanged[str].connect(
            self.callback_room_currentIndexChanged)
        self.floor.currentIndexChanged[str].connect(
            self.callback_floor_currentIndexChanged)

        # Set values
        if event:
            self.name.setText(event.name)
        if room:
            self.room.setCurrentIndex(self.room.findText(room.title()))
        if floor:
            self.floor.setCurrentIndex(self.floor.findText(floor.title()))

    def callback_name_textEdited(self, text):
        self.settings["name"] = text

    def callback_room_currentIndexChanged(self, text):
        self.settings["room"] = text.lower()

    def callback_floor_currentIndexChanged(self, text):
        self.settings["floor"] = text.lower()

    def accept(self):
        """Verifies if the values are ready to be submitted"""
        if not self.settings["name"]:
            QtWidgets.QMessageBox.information(self, "Missing Info",
                "Event name required.")
            # event.ignore()
            return
        if not self.settings["room"]:
            QtWidgets.QMessageBox.information(self, "Missing Info",
                "Event room required.")
            # event.ignore()
            return
        if not self.settings["floor"]:
            QtWidgets.QMessageBox.information(self, "Missing Info",
                "Event floor required.")
            # event.ignore()
            return
        super().accept()
