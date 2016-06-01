from functools import lru_cache

from PyQt5 import QtGui, QtWidgets, QtCore

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
            QtWidgets.QPushButton, "monsterImage")
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

        # Disable layout
        layout = self.parent.findChild(QtWidgets.QVBoxLayout, "monsterLayout")
        self.set_enable_layout(layout, False)

        # Set vertical header to visible
        monster_stats.verticalHeader().setVisible(True)

        monster_list.keyPressEvent = self.delete_press_generator(
            "monster", monster_list, self.delete_monster)
        monster_attr_list.keyPressEvent = self.delete_press_generator(
            "attribute", monster_attr_list, self.delete_attribute)
        monster_ability_list.keyPressEvent = self.delete_press_generator(
            "ability", monster_ability_list, self.delete_ability)
        monster_drop_list.keyPressEvent = self.delete_press_generator(
            "drop", monster_drop_list, self.delete_drop)

        # Signals
        monster_list.currentItemChanged.connect(self.set_focus)
        monster_list.currentItemChanged.connect(self.set_dialogue_enable)
        monster_name.editingFinished.connect(self.update_monster_name)
        monster_stats.cellChanged.connect(self.update_monster_stats)
        monster_floor.currentIndexChanged[str].connect(
            self.update_monster_floor)
        monster_image.clicked.connect(self.update_monster_image)
        monster_rating.valueChanged.connect(self.update_monster_rating)
        new_monster.clicked.connect(self.new_monster)
        new_drop.clicked.connect(self.new_monster_drop)
        new_attribute.clicked.connect(self.new_monster_attribute)
        new_ability.clicked.connect(self.new_monster_move)

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
        monster_drops = self.parent.findChild(
            QtWidgets.QListWidget, "monsterDropList")
        monster_drops.clear()
        for drop in monster["drops"]:
            monster_drops.addItem(drop)

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
            w = min(img.width(), monster_image.width());
            h = min(img.height(), monster_image.height());
            img = img.scaled(w, h, QtCore.Qt.KeepAspectRatio)
            icon = QtGui.QIcon(img)
            monster_image.setIcon(icon);
            monster_image.setIconSize(img.rect().size());
        else:
            monster_image.setIcon(QtGui.QIcon());

    def set_dialogue_enable(self, next, prev):
        if next != None:
            layout = self.parent.findChild(
                QtWidgets.QVBoxLayout, "monsterLayout")
            self.set_enable_layout(layout, True)

    @staticmethod
    def delete_monster(self, widget_list):
        self.monster_dm.delete_monster(self.focus.text())
        widget_list.takeItem(widget_list.currentRow())

    @staticmethod
    def delete_drop(self, widget_list):
        monster_drops = self.parent.findChild(
            QtWidgets.QListWidget, "monsterDropList")
        drop = monster_attr_list.currentItem().text()
        self.monster_dm.remove_monster_drop(self.focus.text(), drop)
        widget_list.takeItem(widget_list.currentRow())

    @staticmethod
    def delete_attribute(self, widget_list):
        monster_attr_list = self.parent.findChild(
            QtWidgets.QListWidget, "monsterAttrList")
        attr = monster_attr_list.currentItem().text()
        self.monster_dm.remove_monster_attribute(self.focus.text(), attr)
        widget_list.takeItem(widget_list.currentRow())

    @staticmethod
    def delete_ability(self, widget_list):
        monster_ability_list = self.parent.findChild(
            QtWidgets.QListWidget, "monsterAbilityList")
        move = monster_ability_list.currentItem().text()
        self.monster_dm.remove_monster_move(self.focus.text(), move)
        widget_list.takeItem(widget_list.currentRow())

    def new_monster(self):
        monster, ok = QtWidgets.QInputDialog.getText(
            self.parent, 'Add New Monster...', 'Enter monster name:')
        if ok:
            monster_list = self.parent.findChild(
                QtWidgets.QListWidget, "monsterList")
            if not monster_list.findItems(monster, QtCore.Qt.MatchExactly):
                monster_list.addItem(monster)
                self.monster_dm.new_monster(monster)
            else:
                QtWidgets.QMessageBox.warning(
                    self, "Error", "Monster name '%s' already exists." % choice)

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
        file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.parent, 'Open image', filter="Images (*.png *.bmp *.jpg)")
        if file:
            self.monster_dm.update_monster_image(self.focus.text(),
                "neutral", file)
            monster_image = self.parent.findChild(
                QtWidgets.QPushButton, "monsterImage")
            monster = self.monster_dm.get_monster(self.focus.text())
            img = self._load_icon(monster["graphic"]["neutral"])
            w = min(img.width(), monster_image.width());
            h = min(img.height(), monster_image.height());
            img = img.scaled(w, h, QtCore.Qt.KeepAspectRatio)
            icon = QtGui.QIcon(img)
            monster_image.setIcon(icon);
            monster_image.setIconSize(img.rect().size());

    def new_monster_move(self):
        move, ok = QtWidgets.QInputDialog.getText(
            self.parent, 'Add New Move...', 'Enter move name:')
        if ok:
            monster_list = self.parent.findChild(
                QtWidgets.QListWidget, "monsterAbilityList")
            if not monster_list.findItems(move, QtCore.Qt.MatchExactly):
                monster_list.addItem(move)
                self.monster_dm.add_monster_move(self.focus.text(), move)
            else:
                QtWidgets.QMessageBox.warning(
                    self, "Error", "Monster move '%s' already exists." % choice)

    def new_monster_attribute(self):
        attribute, ok = QtWidgets.QInputDialog.getText(
            self.parent, 'Add New Attribute...', 'Enter attribute name:')
        if ok:
            monster_list = self.parent.findChild(
                QtWidgets.QListWidget, "monsterAttrList")
            if not monster_list.findItems(attribute, QtCore.Qt.MatchExactly):
                monster_list.addItem(attribute)
                self.monster_dm.add_monster_attribute(self.focus.text(),
                    attribute)
            else:
                QtWidgets.QMessageBox.warning(
                    self, "Error", "Monster attribute '%s' already exists." % choice)

    def new_monster_drop(self):
        drop, ok = QtWidgets.QInputDialog.getText(
            self.parent, 'Add New Drop...', 'Enter drop name:')
        if ok:
            monster_list = self.parent.findChild(
                QtWidgets.QListWidget, "monsterDropList")
            if not monster_list.findItems(drop, QtCore.Qt.MatchExactly):
                monster_list.addItem(drop)
                self.monster_dm.add_monster_drop(self.focus.text(), drop)
            else:
                QtWidgets.QMessageBox.warning(
                    self, "Error", "Monster drop '%s' already exists." % choice)

    @lru_cache(maxsize=16)
    def _load_icon(self, filename):
        """Convenience function used to load icons taking advantage of
        an LRU cache for faster loading"""
        return QtGui.QPixmap(filename)