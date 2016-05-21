from functools import lru_cache

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

    @lru_cache(maxsize=16)
    def _load_icon(self, filename):
        return QtGui.QPixmap(filename)

    def init_moves(self):
        # Get the all components
        move_list = self.parent.findChild(QtWidgets.QListWidget, "moveList")
        new_move = self.parent.findChild(QtWidgets.QPushButton, "newMove")
        move_icon = self.parent.findChild(QtWidgets.QPushButton, "moveIcon")
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

        move_list.currentItemChanged.connect(self.load_move)


    def load_move(self, item):
        # Get move
        move = self.MOVES[item.text()]

        # Load name
        move_name = self.parent.findChild(QtWidgets.QLineEdit, "moveName")
        move_name.setText(move.name)

        # Load chance, load miss
        move_crit = self.parent.findChild(QtWidgets.QSpinBox, "moveCrit")
        move_crit.setValue(100-move.crit_bound) # Inverted
        move_miss = self.parent.findChild(QtWidgets.QSpinBox, "moveMiss")
        move_miss.setValue(move.miss_bound)

        # Load stat distribution (for level up)
        move_stats = self.parent.findChild(QtWidgets.QTableWidget, "moveStats")
        for i in range(move_stats.rowCount()):
            if move_stats.verticalHeaderItem(i).text() == "Health":
                move_stats.item(i,0).setText(str(move.statdist["health"]))
            elif move_stats.verticalHeaderItem(i).text() == "Attack":
                move_stats.item(i,0).setText(str(move.statdist["attack"]))
            elif move_stats.verticalHeaderItem(i).text() == "Defense":
                move_stats.item(i,0).setText(str(move.statdist["defense"]))
            elif move_stats.verticalHeaderItem(i).text() == "Magic":
                move_stats.item(i,0).setText(str(move.statdist["magic"]))
            elif move_stats.verticalHeaderItem(i).text() == "Resist":
                move_stats.item(i,0).setText(str(move.statdist["resist"]))
            elif move_stats.verticalHeaderItem(i).text() == "Speed":
                move_stats.item(i,0).setText(str(move.statdist["speed"]))
            elif move_stats.verticalHeaderItem(i).text() == "Action":
                move_stats.item(i,0).setText(str(move.statdist["action"]))

        # Load description
        move_desc = self.parent.findChild(QtWidgets.QTextEdit, "moveDesc")
        move_desc.setText(move.description)

        # Load icon
        move_icon = self.parent.findChild(QtWidgets.QPushButton, "moveIcon")
        if move.icon:
            img = self._load_icon(move.icon).scaled(
                move_icon.width(), move_icon.height())
            icon = QtGui.QIcon(img)
            move_icon.setIcon(icon);
            move_icon.setIconSize(img.rect().size());
        else:
            move_icon.setIcon(QtGui.QIcon());

        # Load components
        comp_list = self.parent.findChild(QtWidgets.QListWidget, "compList")
        comp_list.clear()
        for attr in move.components:
            comp_list.addItem(type(attr).__name__)
        # Crit
        crit_list = self.parent.findChild(QtWidgets.QListWidget, "critList")
        crit_list.clear()
        for attr in move.crit_components:
            crit_list.addItem(type(attr).__name__)
        # Miss
        miss_list = self.parent.findChild(QtWidgets.QListWidget, "missList")
        miss_list.clear()
        for attr in move.miss_components:
            miss_list.addItem(type(attr).__name__)