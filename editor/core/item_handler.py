from PyQt5 import QtGui, QtWidgets, QtCore

import assets.attributes
from editor.core.class_prompt import ClassPrompt
from engine.game.item import item
from engine.serialization.serialization import deserialize

class ItemHandler:
    """Class responsible for handling item editing"""
    BASE_ITEMS = {} # storage for the item data
    ITEMS = {}
    ITEM_SETS = {}

    def __init__(self, parent):
        self.parent = parent
        self.init_items()
        self.current_focus = None

    def init_items(self):
        self.BASE_ITEMS = deserialize("data/item/base_items.p")
        self.ITEMS = deserialize("data/item/items.p")
        self.ITEM_SETS = deserialize("data/item/item_sets.p")

        item_base = self.parent.findChild(QtWidgets.QRadioButton, "base")
        item_name = self.parent.findChild(QtWidgets.QLineEdit, "itemName")
        item_list = self.parent.findChild(QtWidgets.QListWidget, "itemList")
        item_layout = self.parent.findChild(QtWidgets.QVBoxLayout, "itemBox")
        item_type = self.parent.findChild(QtWidgets.QComboBox, "itemType")
        item_slot = self.parent.findChild(QtWidgets.QComboBox, "itemSlot")
        item_stats = self.parent.findChild(QtWidgets.QTableWidget, "itemStats")
        attr_button = self.parent.findChild(
            QtWidgets.QPushButton, "attrButton")
        attr_list = self.parent.findChild(QtWidgets.QListWidget, "attrList")

        # Set vertical header to visible
        item_stats.verticalHeader().setVisible(True)

        # Load base items to itemList
        for item in self.BASE_ITEMS.keys():
            item_list.addItem(item)

        # Load other items to itemList
        for item in self.ITEMS.keys():
            item_list.addItem(item)

        # Disable item editing by default
        self.set_enable_layout(item_layout, False)

        # Add key press event
        item_list.keyPressEvent = self.item_key_press
        attr_list.keyPressEvent = self.attribute_key_press

        # Add slot to list signal
        item_base.toggled.connect(self.update_item_base)
        item_name.textEdited.connect(self.update_item_name)
        item_list.currentItemChanged.connect(self.set_item_enable)
        item_list.currentItemChanged.connect(self.load_item)
        item_stats.cellChanged.connect(self.update_item_stats)
        item_type.currentIndexChanged[str].connect(self.update_item_type)
        item_slot.currentIndexChanged[str].connect(self.update_item_slot)
        attr_button.clicked.connect(self.new_attribute)

    def item_key_press(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            item_list = self.parent.findChild(
                QtWidgets.QListWidget, "itemList")
            if item_list.selectedItems():
                reponse = QtWidgets.QMessageBox.question(self.parent, "Delete",
                    "Do you want to delete this item?")
                if reponse == QtWidgets.QMessageBox.Yes:
                    if self.BASE_ITEMS.get(self.current_focus.text()):
                        del self.BASE_ITEMS[self.current_focus.text()]
                    elif self.ITEMS.get(self.current_focus.text()):
                        del self.ITEMS[self.current_focus.text()]
                    item_list.takeItem(item_list.currentRow())

    def attribute_key_press(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            attr_list = self.parent.findChild(
                QtWidgets.QListWidget, "attrList")
            if attr_list.selectedItems():
                reponse = QtWidgets.QMessageBox.question(self.parent, "Delete",
                    "Do you want to delete this attribute?")
                if reponse == QtWidgets.QMessageBox.Yes:
                    if self.BASE_ITEMS.get(self.current_focus.text()):
                        item = self.BASE_ITEMS[self.current_focus.text()]
                    elif self.ITEMS.get(self.current_focus.text()):
                        item = self.ITEMS[self.current_focus.text()]
                    del item.attributes[attr_list.currentRow()]
                    attr_list.takeItem(attr_list.currentRow())

    def new_attribute(self):
        prompt = ClassPrompt(self.parent, assets.attributes,
            assets.attributes.Attribute, self.create_attribute)
        prompt.show()

    def create_attribute(self, attribute):
        if self.BASE_ITEMS.get(self.current_focus.text()):
            item = self.BASE_ITEMS[self.current_focus.text()]
        elif self.ITEMS.get(self.current_focus.text()):
            item = self.ITEMS[self.current_focus.text()]
        item.attributes.append(attribute)
        attr_list = self.parent.findChild(QtWidgets.QListWidget, "attrList")
        attr_list.addItem(type(attribute).__name__)

    def set_item_enable(self, next, prev):
        item_layout = self.parent.findChild(QtWidgets.QVBoxLayout, "itemBox")
        self.set_enable_layout(item_layout, True)

    def update_item_base(self, is_base):
        if is_base:
            if self.ITEMS.get(self.current_focus.text()):
                item = self.ITEMS[self.current_focus.text()]
                del self.ITEMS[self.current_focus.text()]
                self.BASE_ITEMS[self.current_focus.text()] = item
        else:
            if self.BASE_ITEMS.get(self.current_focus.text()):
                item = self.BASE_ITEMS[self.current_focus.text()]
                del self.BASE_ITEMS[self.current_focus.text()]
                self.ITEMS[self.current_focus.text()] = item

    def update_item_name(self, name):
        if self.BASE_ITEMS.get(self.current_focus.text()):
            item = self.BASE_ITEMS[self.current_focus.text()]
            item.name = name
            del self.BASE_ITEMS[self.current_focus.text()]
            self.current_focus.setText(name)
            self.BASE_ITEMS[name] = item
        elif self.ITEMS.get(self.current_focus.text()):
            item = self.ITEMS[self.current_focus.text()]
            item.name = name
            del self.ITEMS[self.current_focus.text()]
            self.current_focus.setText(name)
            self.ITEMS[name] = item

    def update_item_stats(self, row, column):
        if self.BASE_ITEMS.get(self.current_focus.text()):
            item = self.BASE_ITEMS[self.current_focus.text()]
        elif self.ITEMS.get(self.current_focus.text()):
            item = self.ITEMS[self.current_focus.text()]
        item_stats = self.parent.findChild(QtWidgets.QTableWidget, "itemStats")
        stype = item_stats.verticalHeaderItem(row).text().lower()
        item.stats[stype] = int(float(item_stats.item(row, column).text()))

    def update_item_type(self, itype):
        if self.BASE_ITEMS.get(self.current_focus.text()):
            item = self.BASE_ITEMS[self.current_focus.text()]
        elif self.ITEMS.get(self.current_focus.text()):
            item = self.ITEMS[self.current_focus.text()]
        item.itype = itype

    def update_item_slot(self, slot):
        if self.BASE_ITEMS.get(self.current_focus.text()):
            item = self.BASE_ITEMS[self.current_focus.text()]
        elif self.ITEMS.get(self.current_focus.text()):
            item = self.ITEMS[self.current_focus.text()]
        item.slot = slot

    def load_item(self, itemname, prev):
        self.current_focus = itemname

        # Technically you can have a name corresponding to both
        # a base and non-base item so this is bad
        if self.BASE_ITEMS.get(self.current_focus.text()):
            item = self.BASE_ITEMS[self.current_focus.text()]
            base = True
        elif self.ITEMS.get(self.current_focus.text()):
            item = self.ITEMS[self.current_focus.text()]
            base = False

        if(base):
            item_base = self.parent.findChild(QtWidgets.QRadioButton, "base")
            item_base.setChecked(True)
        else:
            item_base = self.parent.findChild(QtWidgets.QRadioButton, "nonbase")
            item_base.setChecked(True)

        item_name = self.parent.findChild(QtWidgets.QLineEdit, "itemName")
        item_name.setText(item.name)

        item_type = self.parent.findChild(QtWidgets.QComboBox, "itemType")
        item_type.setCurrentIndex(item_type.findText(item.itype.title()))

        item_slot = self.parent.findChild(QtWidgets.QComboBox, "itemSlot")
        item_slot.setCurrentIndex(item_slot.findText(item.slot.title()))

        attr_list = self.parent.findChild(QtWidgets.QListWidget, "attrList")
        attr_list.clear()
        for attr in item.attributes:
            attr_list.addItem(type(attr).__name__)

        item_stats = self.parent.findChild(QtWidgets.QTableWidget, "itemStats")
        for i in range(item_stats.rowCount()):
            if item_stats.verticalHeaderItem(i).text() == "Health":
                item_stats.item(i,0).setText(str(item.stats["health"]))
            elif item_stats.verticalHeaderItem(i).text() == "Attack":
                item_stats.item(i,0).setText(str(item.stats["attack"]))
            elif item_stats.verticalHeaderItem(i).text() == "Defense":
                item_stats.item(i,0).setText(str(item.stats["defense"]))
            elif item_stats.verticalHeaderItem(i).text() == "Magic":
                item_stats.item(i,0).setText(str(item.stats["magic"]))
            elif item_stats.verticalHeaderItem(i).text() == "Resist":
                item_stats.item(i,0).setText(str(item.stats["resist"]))
            elif item_stats.verticalHeaderItem(i).text() == "Speed":
                item_stats.item(i,0).setText(str(item.stats["speed"]))
            elif item_stats.verticalHeaderItem(i).text() == "Action":
                item_stats.item(i,0).setText(str(item.stats["action"]))

    def set_enable_layout(self, layout, enable):
        """Disables or enables all children in the dialogueLayout"""
        for i in range(layout.count()):
            if isinstance(layout.itemAt(i), QtWidgets.QLayout):
                self.set_enable_layout(layout.itemAt(i), enable)
            else:
                if hasattr(layout.itemAt(i).widget(), "setEnabled"):
                    layout.itemAt(i).widget().setEnabled(enable)