from functools import lru_cache

from PyQt5 import QtGui, QtWidgets

from editor.core.handler.handler import Handler
from engine.serialization.floor import FloorDataManager
from engine.serialization.serialization import deserialize

class MonsterHandler(Handler):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        # Load data
        self.floor = FloorDataManager()
        self.MONSTER_DEFS = deserialize("data/monster.p")

        # Get relevant widgets
        monster_list = self.parent.findChild(
            QtWidgets.QListWidget, "monsterList")
        monster_image = self.parent.findChild(
            QtWidgets.QGraphicsView, "monsterImage")
        monster_drop_list = self.parent.findChild(
            QtWidgets.QListWidget, "monsterDropList")
        monster_name = self.parent.findChild(
            QtWidgets.QLineEdit, "monsterName")
        monster_floor = self.parent.findChild(
            QtWidgets.QComboBox, "monsterFloor")
        monster_stats = self.parent.findChild(
            QtWidgets.QTableWidget, "monsterStats")
        monster_attr_list = self.parent.findChild(
            QtWidgets.QListWidget, "monsterAttrList")
        monster_ability_list = self.parent.findChild(
            QtWidgets.QListWidget, "monsterAbilityList")
        new_drop = self.parent.findChild(
            QtWidgets.QPushButton, "newDrop")
        new_attribute = self.parent.findChild(
            QtWidgets.QPushButton, "newAttribute")
        new_ability = self.parent.findChild(
            QtWidgets.QPushButton, "newAbility")
        new_monster = self.parent.findChild(
            QtWidgets.QPushButton, "newMonster")

        # Load list
        for monster_name in self.MONSTER_DEFS:
            monster_list.addItem(monster_name)

        # Load floors
        monster_floor.clear()
        for floor in self.floor.floors():
            monster_floor.addItem(floor)

        # Set vertical header to visible
        monster_stats.verticalHeader().setVisible(True)

        # Signals
        monster_list.currentItemChanged.connect(self.set_focus)

    def change_focus(self, focus):
        monster = self._get_monster_def(focus.text())

        # Load name
        monster_name = self.parent.findChild(
            QtWidgets.QLineEdit, "monsterName")
        monster_name.setText(focus.text())

        # Load location
        monster_floor = self.parent.findChild(
            QtWidgets.QComboBox, "monsterFloor")
        monster_floor.setCurrentIndex(
            monster_floor.findText(monster["location"]))

        # Load Stats
        monster_stats = self.parent.findChild(
            QtWidgets.QTableWidget, "monsterStats")
        for i in range(monster_stats.rowCount()):
            if monster_stats.verticalHeaderItem(i).text() == "Health":
                monster_stats.item(i,0).setText(
                    str(monster["stats"]["health"]))
            elif monster_stats.verticalHeaderItem(i).text() == "Attack":
                monster_stats.item(i,0).setText(
                    str(monster["stats"]["attack"]))
            elif monster_stats.verticalHeaderItem(i).text() == "Defense":
                monster_stats.item(i,0).setText(
                    str(monster["stats"]["defense"]))
            elif monster_stats.verticalHeaderItem(i).text() == "Magic":
                monster_stats.item(i,0).setText(
                    str(monster["stats"]["magic"]))
            elif monster_stats.verticalHeaderItem(i).text() == "Resist":
                monster_stats.item(i,0).setText(
                    str(monster["stats"]["resist"]))
            elif monster_stats.verticalHeaderItem(i).text() == "Speed":
                monster_stats.item(i,0).setText(
                    str(monster["stats"]["speed"]))

        # Load drops
        # Not yet implemented

        # Load Abilities
        monster_ability_list = self.parent.findChild(
            QtWidgets.QListWidget, "monsterAbilityList")
        monster_ability_list.clear()
        for ability in monster["abilities"]:
            monster_ability_list.addItem(ability)

        # Load Attributes
        monster_attr_list = self.parent.findChild(
            QtWidgets.QListWidget, "monsterAttrList")
        monster_attr_list.clear()
        for attr in monster["attributes"]:
            monster_attr_list.addItem(attr)

        # Load icon
        monster_image = self.parent.findChild(
            QtWidgets.QPushButton, "monsterImage")
        if monster["graphic"]:
            img = self._load_icon(monster["graphic"]["neutral"])
            w = min(img.width(), monster_image.maximumWidth());
            h = min(img.height(), monster_image.maximumHeight());
            icon = QtGui.QIcon(img.scaled(w, h))
            monster_image.setIcon(icon);
            monster_image.setIconSize(img.rect().size());
        else:
            monster_image.setIcon(QtGui.QIcon());

    def _get_monster_def(self, name):
        """Convenience function used to get the monster definition"""
        return self.MONSTER_DEFS.get(name)

    @lru_cache(maxsize=16)
    def _load_icon(self, filename):
        """Convenience function used to load icons taking advantage of
        an LRU cache for faster loading"""
        return QtGui.QPixmap(filename)