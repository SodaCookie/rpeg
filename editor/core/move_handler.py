from PyQt5 import QtGui, QtWidgets, QtCore

import assets.moves
import assets.moves.components
import assets.moves.modifiers

from editor.core.class_prompt import ClassPrompt
from engine.serialization.serialization import deserialize

class MoveHandler:

    def __init__(self, parent):
        self.parent = parent
        self.MOVES = deserialize("data/moves.p")
        self.init_moves()
        self.current_focus = None

    def init_moves(self):
        # Get the all components
        move_list = self.parent.findChild(QtWidgets.QListWidget, "moveList")
        new_move = self.parent.findChild(QtWidgets.QPushButton, "newMove")
        move_icon = self.parent.findChild(QtWidgets.QGraphicsView, "moveIcon")
        move_name = self.parent.findChild(QtWidgets.QLineEdit, "moveName")
        move_crit = self.parent.findChild(QtWidgets.QSpinBox, "moveCrit")
        move_miss = self.parent.findChild(QtWidgets.QSpinBox, "moveMiss")
        move_desc = self.parent.findChild(QtWidgets.QTextEdit, "moveDesc")
        move_stats = self.parent.findChild(QtWidgets.QTableWidget, "moveStats")
        mod_list = self.parent.findChild(
            QtWidgets.QListWidget, "modifierList")
        new_mod = self.parent.findChild(QtWidgets.QPushButton, "newModifier")
        new_component = self.parent.findChild(
            QtWidgets.QPushButton, "newComponent")

        # Set vertical header to visible
        move_stats.verticalHeader().setVisible(True)

        # Populate move list
        for move in self.MOVES:
            move_list.addItem(move)


    def load_move(self, item):
        pass