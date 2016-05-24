from functools import lru_cache

from PyQt5 import QtGui, QtWidgets, QtCore

import assets.moves
import assets.moves.components
import assets.moves.modifiers

from editor.core.class_prompt import ClassPrompt
from editor.meta.typecheck import typecheck
from editor.meta.valuecheck import valuecheck, value_from_type
from editor.meta.types import *
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
        components_table = self.parent.findChild(
            QtWidgets.QTreeWidget, "componentList")
        components_table.clear()

        item = QtWidgets.QTreeWidgetItem(["<Components>"])
        components_table.addTopLevelItem(item)
        for component in move.components:
            self._load_components(item, component)
        item.setExpanded(True)

        item = QtWidgets.QTreeWidgetItem(["<MissComponents>"])
        components_table.addTopLevelItem(item)
        for component in move.miss_components:
            self._load_components(item, component)
        item.setExpanded(True)

        item = QtWidgets.QTreeWidgetItem(["<CritComponents>"])
        components_table.addTopLevelItem(item)
        for component in move.crit_components:
            self._load_components(item, component)
        item.setExpanded(True)

    def _load_components(self, item, component):
        """Recursive convenience function for loading in components into
        a higher level component"""
        component_item = QtWidgets.QTreeWidgetItem([type(component).__name__])
        item.addChild(component_item)
        parameters = typecheck(type(component))
        for parameter, ptype in parameters.items():
            # Parameter item
            para_item = QtWidgets.QTreeWidgetItem(
                ["%s : <%s>" % (parameter, str(ptype))])
            component_item.addChild(para_item)
            # Attempt to fill in the value
            value = valuecheck(component, parameter)
            if value != None:
                self._load_parameter(para_item, ptype, value)
            else:
                para_item.addChild(QtWidgets.QTreeWidgetItem(
                    [""]))

            # Recover type if value is known
            if type(ptype) == UnknownType and value != None:
                para_item.takeChildren()
                derived_type = value_from_type(value)
                self._load_parameter(para_item, derived_type, value)
                para_item.setText(0, "%s : <%s>" % (parameter,
                    str(derived_type)))

    def _load_parameter(self, item, ptype, value):
        """Convenience function for loading parameters"""
        if isinstance(ptype, ListType): # if our type is a list
            for subcomponent in value:
                self._load_components(item, subcomponent)
        elif isinstance(ptype, LambdaType):
            item.addChild(QtWidgets.QTreeWidgetItem(
                ["<function>"]))
        elif isinstance(ptype,
                (EffectType, ComponentType, ModifierType, AttributeType)):
            self._load_components(item, value)
        else:
            item.addChild(QtWidgets.QTreeWidgetItem(
                [str(value)]))