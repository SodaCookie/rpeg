from PyQt5 import QtGui, QtWidgets, QtCore

import assets.attributes

from editor.core.handler.handler import Handler
from editor.core.prompt.class_prompt import ClassPrompt
from engine.game.item import item
from engine.serialization.item import ItemDataManager

class ItemHandler(Handler):
    """Class responsible for handling item editing"""

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        self.itemdm = ItemDataManager()

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
        for item in self.itemdm.base_items().keys():
            item_list.addItem(item)

        # Load other items to itemList
        for item in self.itemdm.items().keys():
            item_list.addItem(item)

        # Disable item editing by default
        self.set_enable_layout(item_layout, False)

        # Add key press event
        item_list.keyPressEvent = self.delete_press_generator(
            "item", item_list, self.delete_item)
        attr_list.keyPressEvent = self.delete_press_generator(
            "attribute", attr_list, self.delete_attribute)

        # Add slot to list signal
        item_base.toggled.connect(self.update_item_base)
        item_name.editingFinished.connect(self.update_item_name)
        item_list.currentItemChanged.connect(self.set_item_enable)
        item_list.currentItemChanged.connect(self.set_focus)
        item_stats.cellChanged.connect(self.update_item_stats)
        item_type.currentIndexChanged[str].connect(self.update_item_type)
        item_slot.currentIndexChanged[str].connect(self.update_item_slot)
        attr_button.clicked.connect(self.new_attribute)

    @staticmethod
    def delete_item(self, widget_list):
        self.itemdm.delete_item(self.focus.text())
        widget_list.takeItem(widget_list.currentRow())

    @staticmethod
    def delete_attribute(self, widget_list):
        self.itemdm.remove_item_attribute(self.focus.text(),
            widget_list.currentRow())
        widget_list.takeItem(widget_list.currentRow())

    def new_attribute(self):
        prompt = ClassPrompt(self.parent, assets.attributes,
            assets.attributes.Attribute, self.create_attribute)
        prompt.show()

    def create_attribute(self, attribute):
        self.itemdm.add_item_attribute(self.focus.text(), attribute)
        attr_list = self.parent.findChild(QtWidgets.QListWidget, "attrList")
        attr_list.addItem(type(attribute).__name__)

    def set_item_enable(self, next, prev):
        item_layout = self.parent.findChild(QtWidgets.QVBoxLayout, "itemBox")
        self.set_enable_layout(item_layout, True)

    def update_item_base(self, is_base):
        self.itemdm.set_item_base(self.focus.text(), is_base)

    def update_item_name(self):
        item_name = self.parent.findChild(QtWidgets.QLineEdit, "itemName")
        self.itemdm.update_item_name(self.focus.text(), item_name.text())
        self.focus.setText(item_name.text())

    def update_item_stats(self, row, column):
        item_stats = self.parent.findChild(QtWidgets.QTableWidget, "itemStats")
        stype = item_stats.verticalHeaderItem(row).text().lower()
        value = int(float(item_stats.item(row, column).text()))
        self.itemdm.update_item_stat(self.focus.text(), stype, value)

    def update_item_type(self, itype):
        self.itemdm.update_item_type(self.focus.text(), itype.lower())

    def update_item_slot(self, slot):
        self.itemdm.update_item_slot(self.focus.text(), slot.lower())

    def change_focus(self, focus):
        # Technically you can have a name corresponding to both
        # a base and non-base item so this is bad
        item = self.itemdm.get_item(focus.text())

        if(self.itemdm.is_base(item.name)):
            item_base = self.parent.findChild(
                QtWidgets.QRadioButton, "base")
        else:
            item_base = self.parent.findChild(
                QtWidgets.QRadioButton, "nonbase")
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
            stype = item_stats.verticalHeaderItem(i).text().lower()
            item_stats.item(i,0).setText(str(item.stats[stype]))
