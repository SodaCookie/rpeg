from functools import lru_cache, partial
import traceback
import re

from PyQt5 import QtGui, QtWidgets, QtCore

import assets.moves.components
import assets.moves.modifiers
import assets.attributes
import assets.effects
import assets.actions

from editor.core.handler.handler import Handler
from editor.core.prompt.class_prompt import ClassPrompt
from editor.core.prompt.list_prompt import ListPrompt
from editor.meta.typecheck import typecheck, get_type
from editor.meta.valuecheck import valuecheck, value_from_type, assign_value
from editor.meta.types import *
from editor.core.prompt import class_prompt
from engine.game.move.move import Move
from engine.game.move.component import Component
from engine.serialization.move import MoveDataManager


from engine.game.move.component import Component
from engine.game.attribute.attribute import Attribute
from engine.game.effect.effect import Effect
from engine.game.dungeon.action import Action
from engine.game.move.modifier import Modifier

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
        components_table = self.parent.findChild(
            QtWidgets.QTreeWidget, "componentList")

        # Set vertical header to visible
        move_stats.verticalHeader().setVisible(True)

        # Disable layout
        layout = self.parent.findChild(QtWidgets.QVBoxLayout, "moveLayout")
        self.set_enable_layout(layout, False)

        # Populate move list
        for move in self.move_dm.moves():
            move_list.addItem(move)

        move_list.keyPressEvent = self.delete_press_generator("move",
            move_list, self.delete_move)

        move_list.currentItemChanged.connect(self.set_focus)
        move_list.currentItemChanged.connect(self.set_dialogue_enable)
        move_name.editingFinished.connect(self.update_move_name)
        move_crit.valueChanged.connect(self.update_move_crit_chance)
        move_miss.valueChanged.connect(self.update_move_miss_chance)
        move_desc.textChanged.connect(self.update_move_description)
        move_stats.cellChanged.connect(self.update_move_statdist)
        move_icon.clicked.connect(self.update_move_icon)
        components_table.customContextMenuRequested.connect(self.load_context)
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
        item.setData(0, QtCore.Qt.UserRole, move)
        components_table.addTopLevelItem(item)
        for component in move.components:
            self._load_components(item, component)
        item.setExpanded(True)

        item = QtWidgets.QTreeWidgetItem(["<MissComponents>"])
        item.setData(0, QtCore.Qt.UserRole, move)
        components_table.addTopLevelItem(item)
        for component in move.miss_components:
            self._load_components(item, component)
        item.setExpanded(True)

        item = QtWidgets.QTreeWidgetItem(["<CritComponents>"])
        item.setData(0, QtCore.Qt.UserRole, move)
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

    def load_context(self, point):
        """Helper function to load the proper context menu for a component"""
        components_table = self.parent.findChild(
            QtWidgets.QTreeWidget, "componentList")
        global_point = components_table.mapToGlobal(point)
        item = components_table.itemAt(point)
        if item is not None:
            parent_data = None
            item_data = item.data(0, QtCore.Qt.UserRole)

            menu = QtWidgets.QMenu(self.parent)
            if item.parent():
                parent_data = item.parent().data(0, QtCore.Qt.UserRole)

            item_type = value_from_type(item_data) # Bugged
            parent_type = value_from_type(parent_data)

            # Add context menu actions
            if isinstance(item_type, ListType):
                # Add to list
                action = QtWidgets.QAction(
                    "Add " + str(item_type.elemtype).title(), self.parent)
                action.setData((item_data, parent_data, item))
                menu.addAction(action)
            if isinstance(item_data, Move):
                # Top level widget
                action = QtWidgets.QAction("Add Component", self.parent)
                action.setData((item_data, parent_data, item))
                menu.addAction(action)
            if isinstance(parent_type, ListType) or \
                    isinstance(parent_data, Move):
                # Remove from a list
                action = QtWidgets.QAction("Remove", self.parent)
                action.setData((item_data, parent_data, item))
                menu.addAction(action)
            # Edge end cases and component lists
            if isinstance(item_type, (UnknownType, IntType, StrType,
                    FloatType, LambdaType)) and item_data is not None and \
                    not isinstance(item_data, Move):
                # Update value
                action = QtWidgets.QAction("Modify", self.parent)
                action.setData((item_data, parent_data, item))
                menu.addAction(action)

            if menu.actions():
                menu.triggered.connect(self.dispatch_component_action)
                menu.exec_(global_point)

    def dispatch_component_action(self, action):
        item_data, parent_data, item = action.data()
        if action.text() == "Remove":
            if isinstance(parent_data, Move):
                # Remove component from list
                if item.parent().text(0) == "<Components>":
                    parent_data.components.remove(item_data)
                elif item.parent().text(0) == "<MissComponents>":
                    parent_data.miss_components.remove(item_data)
                elif item.parent().text(0) == "<CritComponents>":
                    parent_data.crit_components.remove(item_data)
                item.parent().removeChild(item)
            else:
                parent_data.remove(item_data)
                item.parent().removeChild(item)
        elif action.text() == "Modify":
            match = re.match(r"(\w+) : <(.+)>", item.text(0))
            if match:
                parameter = match.group(1)
                type_hint = match.group(2)
                if type_hint == "float":
                    itype = FloatType()
                elif type_hint == "int":
                    itype = IntType()
                elif type_hint == "str":
                    itype = StrType()
                else:
                    itype = value_from_type(item_data)

                if isinstance(itype, UnknownType):
                    code, ok = QtWidgets.QInputDialog.getText(
                        self.parent, 'Modify', 'Python code:')
                    if ok:
                        try:
                            value = eval(code)
                            assign_value(parent_data, parameter, value)
                        except:
                            QtWidgets.QMessageBox.warning(
                                self.parent,
                                "Python Error",
                                traceback.format_exc())
                        item.child(0).setText(0, str(value))
                elif isinstance(itype, IntType):
                    value, ok = QtWidgets.QInputDialog.getInt(
                        self.parent, 'Modify', ' Integer:')
                    if ok:
                        assign_value(parent_data, parameter, value)
                        item.child(0).setText(0, str(value))
                elif isinstance(itype, FloatType):
                    value, ok = QtWidgets.QInputDialog.getDouble(
                        self.parent, 'Modify', ' Float:')
                    if ok:
                        assign_value(parent_data, parameter, value)
                        item.child(0).setText(0, str(value))
                elif isinstance(itype, StrType):
                    value, ok = QtWidgets.QInputDialog.getText(
                        self.parent, 'Modify', ' String:')
                    if ok:
                        assign_value(parent_data, parameter, value)
                        item.child(0).setText(0, str(value))
                elif isinstance(itype, LambdaType):
                    code, ok = QtWidgets.QInputDialog.getText(
                        self.parent, 'Modify', 'Python code:')
                    if ok:
                        try:
                            value = eval(code)
                            assign_value(parent_data, parameter, value)
                        except:
                            QtWidgets.QMessageBox.warning(
                                self.parent,
                                "Python Error",
                                traceback.format_exc())
        else:
            if isinstance(item_data, Move):
                # Add component to list
                if item.text(0) == "<Components>":
                    prompt = ClassPrompt(self.parent, assets.moves.components,
                        Component, partial(self._add_standard_component, item))
                    prompt.show()
                elif item.text(0) == "<MissComponents>":
                    prompt = ClassPrompt(self.parent, assets.moves.components,
                        Component, partial(self._add_miss_component, item))
                    prompt.show()
                elif item.text(0) == "<CritComponents>":
                    prompt = ClassPrompt(self.parent, assets.moves.components,
                        Component, partial(self._add_crit_component, item))
                    prompt.show()
            else:
                # Adding to component list
                match = re.match(r"(\w+) : <(.+)>", item.text(0))
                itype = ListType(UnknownType())
                if match:
                    itype = get_type(match.group(2))
                etype = itype.elemtype

                if isinstance(etype, IntType):
                    value, ok = QtWidgets.QInputDialog.getInt(
                        self.parent, 'Modify', ' Integer:')
                    if ok:
                        item_data.append(value)
                        self._load_parameter(item, etype, value)
                elif isinstance(etype, FloatType):
                    value, ok = QtWidgets.QInputDialog.getDouble(
                        self.parent, 'Modify', ' Float:')
                    if ok:
                        item_data.append(value)
                        self._load_parameter(item, etype, value)
                elif isinstance(etype, StrType):
                    value, ok = QtWidgets.QInputDialog.getText(
                        self.parent, 'Modify', ' String:')
                    if ok:
                        item_data.append(value)
                        self._load_parameter(item, etype, value)
                elif isinstance(etype, LambdaType):
                    code, ok = QtWidgets.QInputDialog.getText(
                        self.parent, 'Modify', 'Python code:')
                    if ok:
                        try:
                            value = eval(code)
                            item_data.append(value)
                            self._load_parameter(item, etype, value)
                        except:
                            QtWidgets.QMessageBox.warning(
                                self.parent,
                                "Python Error",
                                traceback.format_exc())
                elif isinstance(etype, ListType):
                    prompt = editor.core.prompt.list_prompt.ListPrompt(
                        self, etype.elemtype, item_data,
                        partial(self._add_standard_component, item))
                    prompt.show()
                elif isinstance(etype, ComponentType):
                    prompt = ClassPrompt(self.parent, assets.moves.components,
                        Component, partial(self._add_standard_component, item))
                    prompt.show()
                elif isinstance(etype, AttributeType):
                    prompt = ClassPrompt(self.parent, assets.attributes,
                        Attribute, partial(self.add_to_list, item_data))
                    prompt.show()
                elif isinstance(etype, EffectType):
                    prompt = ClassPrompt(self.parent, assets.effects,
                        Effect, partial(self.add_to_list, item_data))
                    prompt.show()
                elif isinstance(etype, ModifierType):
                    prompt = ClassPrompt(self.parent, assets.moves.modifiers,
                        Modifier, partial(self.add_to_list, item_data))
                    prompt.show()
                elif isinstance(etype, UnknownType):
                    code, ok = QtWidgets.QInputDialog.getText(
                        self.parent, 'Modify', 'Python code:')
                    if ok:
                        try:
                            value = eval(code)
                            assign_value(parent_data, parameter, value)
                        except:
                            QtWidgets.QMessageBox.warning(
                                self.parent,
                                "Python Error",
                                traceback.format_exc())
                        item_data.append(value)
                        self._load_parameter(item, etype, value)

    def add_to_list(self, li, item):
        """General purpose function to add an object to a list"""
        li.append(item)

    def _add_standard_component(self, item, component):
        """Helper function to add objects to lists and what not"""
        self.move_dm.add_standard_component(self.focus.text(), component)
        self._load_components(item, component)

    def _add_miss_component(self, item, component):
        """Helper function to add objects to lists and what not"""
        self.move_dm.add_miss_component(self.focus.text(), component)
        self._load_components(item, component)

    def _add_crit_component(self, item, component):
        """Helper function to add objects to lists and what not"""
        self.move_dm.add_crit_component(self.focus.text(), component)
        self._load_components(item, component)

    def _add_asset(self, item, asset_list, asset):
        """Helper function to add objects to lists and what not"""
        asset_list.append(asset)
        self._load_components(item, asset)

    def _load_components(self, item, component):
        """Recursive convenience function for loading in components into
        a higher level component"""
        component_item = QtWidgets.QTreeWidgetItem([type(component).__name__])
        component_item.setData(0, QtCore.Qt.UserRole, component)
        item.addChild(component_item)
        parameters = typecheck(type(component))
        for parameter, ptype in parameters.items():
            # Parameter item
            para_item = QtWidgets.QTreeWidgetItem(
                ["%s : <%s>" % (parameter, str(ptype))])
            component_item.addChild(para_item)
            # Attempt to fill in the value
            value = valuecheck(component, parameter)
            if value is not None:
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
        item.setData(0, QtCore.Qt.UserRole, value)
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

