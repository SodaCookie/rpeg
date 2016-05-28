from functools import lru_cache

from PyQt5 import QtGui, QtWidgets, QtCore

import assets.moves.components
import assets.moves.modifiers

from editor.core.handler.handler import Handler
from editor.core.prompt.class_prompt import ClassPrompt
from editor.meta.typecheck import typecheck
from editor.meta.valuecheck import valuecheck, value_from_type
from editor.meta.types import *
from engine.serialization.move import MoveDataManager

class MoveHandler(Handler):

    def __init__(self, parent):
        super().__init__(parent)

    @lru_cache(maxsize=16)
    def _load_icon(self, filename):
        return QtGui.QPixmap(filename)

    def setup(self):
        self.move_dm = MoveDataManager()

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

        # Disable layout
        layout = self.parent.findChild(QtWidgets.QVBoxLayout, "moveLayout")
        self.set_enable_layout(layout, False)

        # Populate move list
        for move in self.move_dm.moves():
            move_list.addItem(move)

        move_list.currentItemChanged.connect(self.set_focus)
        move_list.currentItemChanged.connect(self.set_dialogue_enable)
        move_name.editingFinished.connect(self.update_move_name)
        move_crit.valueChanged.connect(self.update_move_crit_chance)
        move_miss.valueChanged.connect(self.update_move_miss_chance)
        move_desc.textChanged.connect(self.update_move_description)
        move_stats.cellChanged.connect(self.update_move_statdist)
        move_icon.clicked.connect(self.update_move_icon)
        # move_components
        new_move.clicked.connect(self.create_move)

    def change_focus(self, item):
        # Get move
        move = self.move_dm.moves()[item.text()]

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

    def set_dialogue_enable(self, next, prev):
        if next != None:
            layout = self.parent.findChild(
                QtWidgets.QVBoxLayout, "moveLayout")
            self.set_enable_layout(layout, True)

    @staticmethod
    def delete_move(self, widget_list):
        self.move_dm.delete_move(self.focus.text())
        widget_list.takeItem(widget_list.currentRow())

    def update_move_name(self):
        move_name = self.parent.findChild(
            QtWidgets.QLineEdit, "moveName")
        self.move_dm.update_move_name(self.focus.text(),
            move_name.text())
        self.focus.setText(move_name.text())

    def update_move_crit_chance(self, value):
        self.move_dm.update_move_crit_bound(self.focus.text(), 100 - value)

    def update_move_miss_chance(self, value):
        self.move_dm.update_move_miss_bound(self.focus.text(), value)

    def update_move_description(self):
        move_desc = self.parent.findChild(QtWidgets.QTextEdit, "moveDesc")
        self.move_dm.update_move_description(self.focus.text(),
            move_desc.toPlainText())

    def update_move_statdist(self, row, column):
        move_stats = self.parent.findChild(
            QtWidgets.QTableWidget, "moveStats")
        stype = move_stats.verticalHeaderItem(row).text().lower()
        value = int(float(move_stats.item(row, column).text()))
        self.move_dm.update_move_statdist(self.focus.text(), stype, value)

    def update_move_icon(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.parent, 'Open image', filter="Images (*.png *.bmp *.jpg)")
        if file:
            move_icon = self.parent.findChild(
                QtWidgets.QPushButton, "moveIcon")
            move = self.move_dm.get_move(self.focus.text())
            # Set and draw
            self.move_dm.update_move_icon(self.focus.text(), file)
            img = self._load_icon(move.icon).scaled(
                move_icon.width(), move_icon.height())
            icon = QtGui.QIcon(img)
            move_icon.setIcon(icon);
            move_icon.setIconSize(img.rect().size());

    def create_move(self):
        move_name, ok = QtWidgets.QInputDialog.getText(
            self.parent, 'Add New Move...', 'Enter move name:')
        if ok:
            list_widget = self.parent.findChild(
                QtWidgets.QListWidget, "moveList")
            if not list_widget.findItems(move_name, QtCore.Qt.MatchExactly):
                # Create new event
                self.move_dm.new_move(move_name)
                # Add to required widgets
                list_widget.addItem(move_name)
                list_widget.setCurrentRow(list_widget.count()-1)
            else:
                QtWidgets.QMessageBox.warning(
                    self.parent,
                    "Error",
                    "Move name '%s' already exists." % move_name)

    # HANDLE THE TREE WIDGET???

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