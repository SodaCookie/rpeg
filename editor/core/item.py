from PyQt5 import QtGui, QtWidgets, QtCore
from engine.game.item import item
from engine.serialization.serialization import deserialize
from editor.core.floor import FloorHandler

class ItemHandler:
    """Class responsible for handling item editing"""
    BASE_ITEMS = {} # storage for the item data
    ITEMS = {}
    ITEM_SETS = {}

    def __init__(self, parent):
        self.parent = parent
        self.floor_handler = FloorHandler()
        self.init_items()
        self.current_focus = None

    def init_items(self):
        self.BASE_ITEMS = deserialize("data/item/base_items.p")
        self.ITEMS = deserialize("data/item/items.p")
        self.ITEM_SETS = deserialize("data/item/item_sets.p")

        ft_combo_box = self.parent.findChild(QtWidgets.QComboBox, "itemFloorType")
        item_list = self.parent.findChild(QtWidgets.QListWidget, "itemList")
        item_box = self.parent.findChild(QtWidgets.QGroupBox, "itemBox")
        item_box_layout = item_box.layout()

        # Load floor types
        for floor in self.floor_handler.floors():
            ft_combo_box.addItem(floor.title())

        # Load base items to itemList
        for item in self.BASE_ITEMS.keys():
            item_list.addItem(item)

        # Load other items to itemList
        for item in self.ITEMS.keys():
            item_list.addItem(item)

        # Disable item editing by default
        self.set_enable_layout(item_box_layout, False)

        # Add slot to list signal
        item_list.currentItemChanged.connect(self.set_item_enable)
        item_list.currentItemChanged.connect(self.load_item)

    def set_item_enable(self, next, prev):
        item_box = self.parent.findChild(QtWidgets.QGroupBox, "itemBox")
        item_box_layout = item_box.layout()
        self.set_enable_layout(item_box_layout, True)

    def load_item(self, item, prev):
        self.current_focus = item

        # Technically you can have a name corresponding to both
        # a base and non-base item so this is bad
        if self.BASE_ITEMS.get(self.current_focus.text()):
            _item = self.BASE_ITEMS[self.current_focus.text()]
            base = True
        elif self.ITEMS.get(self.current_focus.text()):
            _item = self.ITEMS[self.current_focus.text()]
            base = False

        if(base):
            item_base = self.parent.findChild(QtWidgets.QRadioButton, "base")
            item_base.setChecked(True)
        else:
            item_base = self.parent.findChild(QtWidgets.QRadioButton, "nonbase")
            item_base.setChecked(True)

        item_name = self.parent.findChild(QtWidgets.QLineEdit, "itemName")
        item_name.setText(_item.name)

        item_type = self.parent.findChild(QtWidgets.QComboBox, "itemType")
        item_type.setCurrentIndex(item_type.findText(_item.itype.title()))

        item_slot = self.parent.findChild(QtWidgets.QComboBox, "itemSlot")
        item_slot.setCurrentIndex(item_slot.findText(_item.slot.title()))

        floor = "Any"
        for item_set in self.ITEM_SETS.keys():
            for item in self.ITEM_SETS[item_set]:
                if item == _item.name:
                    floor = item_set
        item_floor = self.parent.findChild(QtWidgets.QComboBox, "itemFloorType")
        if(base):
            item_floor.setEnabled(False)
        else:
            item_floor.setEnabled(True)
            item_floor.setCurrentIndex(item_floor.findText(floor.title()))

        # This is busted with current UI
        item_stats = self.parent.findChild(QtWidgets.QTableWidget, "itemStats")
        for i in range(item_stats.rowCount()):
            print("got here")
            print(item_stats.item(i,0).text())
            if item_stats.item(i,0).text() == "Health":
                item_stats.item(i,1).setText(_item.stats["health"])
            elif item_stats.item(i,0).text() == "Attack":
                item_stats.item(i,1).setText(_item.stats["attack"])
            elif item_stats.item(i,0).text() == "Defense":
                item_stats.item(i,1).setText(_item.stats["defense"])
            elif item_stats.item(i,0).text() == "Magic":
                item_stats.item(i,1).setText(_item.stats["magic"])
            elif item_stats.item(i,0).text() == "Resist":
                item_stats.item(i,1).setText(_item.stats["resist"])
            elif item_stats.item(i,0).text() == "Speed":
                item_stats.item(i,1).setText(_item.stats["speed"])
            elif item_stats.item(i,0).text() == "Action":
                item_stats.item(i,1).setText(_item.stats["action"])

    def set_enable_layout(self, layout, enable):
        """Disables or enables all children in the dialogueLayout"""
        for i in range(layout.count()):
            if isinstance(layout.itemAt(i), QtWidgets.QLayout):
                self.set_enable_layout(layout.itemAt(i), enable)
            else:
                if hasattr(layout.itemAt(i).widget(), "setEnabled"):
                    layout.itemAt(i).widget().setEnabled(enable)