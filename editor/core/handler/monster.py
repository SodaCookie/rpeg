from functools import lru_cache

from PyQt5 import QtGui, QtWidgets

from editor.core.handler.handler import Handler
from engine.serialization.floor import FloorDataManager
from engine.serialization.monster import MonsterDataManager

class MonsterHandler(Handler):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        # Load data
        self.floor = FloorDataManager()
        self.monster_dm = MonsterDataManager()

        # Get relevant widgets
        monster_list = self.parent.findChild(
            QtWidgets.QListWidget, "monsterList")
        monster_image = self.parent.findChild(
            QtWidgets.QGraphicsView, "monsterImage")
        monster_drop_list = self.parent.findChild(
            QtWidgets.QListWidget, "monsterDropList")
        monster_name = self.parent.findChild(
            QtWidgets.QLineEdit, "monsterName")
        monster_rating = self.parent.findChild(
            QtWidgets.QSpinBox, "monsterRating")
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
        for m_name in self.monster_dm.monsters():
            monster_list.addItem(m_name)

        # Load floors
        monster_floor.clear()
        for floor in self.floor.floors():
            monster_floor.addItem(floor)

        # Set vertical header to visible
        monster_stats.verticalHeader().setVisible(True)

        # Signals
        monster_list.currentItemChanged.connect(self.set_focus)
        monster_name.editingFinished.connect(self.update_monster_name)
        monster_stats.cellChanged.connect(self.update_monster_stats)
        monster_floor.currentIndexChanged[str].connect(
            self.update_monster_floor)
        monster_rating.valueChanged.connect(self.update_monster_rating)

    def change_focus(self, focus):
        monster = self.monster_dm.get_monster(focus.text())

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
            stype = monster_stats.verticalHeaderItem(i).text().lower()
            monster_stats.item(i,0).setText(str(monster["stats"][stype]))

        # Load Rating
        monster_rating = self.parent.findChild(
            QtWidgets.QSpinBox, "monsterRating")
        monster_rating.setValue(monster["rating"])

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

    @staticmethod
    def delete_monster(self, widget_list):
        return NotImplemented

    @staticmethod
    def delete_drop(self, widget_list):
        return NotImplemented

    @staticmethod
    def delete_attribute(self, widget_list):
        return NotImplemented

    @staticmethod
    def delete_ability(self, widget_list):
        return NotImplemented

    def update_monster_stats(self, row, column):
        monster_stats = self.parent.findChild(
            QtWidgets.QTableWidget, "monsterStats")
        stype = monster_stats.verticalHeaderItem(row).text().lower()
        value = int(float(monster_stats.item(row, column).text()))
        self.monster_dm.update_monster_stats(self.focus.text(), stype, value)

    def update_monster_name(self):
        monster_name = self.parent.findChild(
            QtWidgets.QLineEdit, "monsterName")
        self.monster_dm.update_monster_name(self.focus.text(),
            monster_name.text())
        self.focus.setText(monster_name.text())

    def update_monster_rating(self, value):
        self.monster_dm.update_monster_rating(self.focus.text(), value)

    def update_monster_floor(self, value):
        self.monster_dm.update_monster_location(self.focus.text(), value)

    def update_monster_location(self, location):
        self.monster_dm.update_monster_location(self.focus.text(),
            location.lower())

    def update_monster_image(self):
        return NotImplemented

    def create_monster_move(self):
        return NotImplemented

    def create_monster_attribute(self):
        return NotImplemented

    def create_monster_drop(self):
        return NotImplemented

    @lru_cache(maxsize=16)
    def _load_icon(self, filename):
        """Convenience function used to load icons taking advantage of
        an LRU cache for faster loading"""
        return QtGui.QPixmap(filename)