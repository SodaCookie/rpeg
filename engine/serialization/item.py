"""Implements the ItemDataManager class"""
import logging

from engine.serialization.dmanager import DataManager
from engine.game.item.item import Item

class ItemDataManager(object):
    """Wrapper class to handle item attributes and items"""

    DEFAULT_ITEM_TYPE = "sword"
    DEFAULT_ITEM_STATS = {
        "attack" : 0,
        "speed" : 0,
        "defense" : 0,
        "health" : 0,
        "magic" : 0,
        "resist" : 0,
        "action" : 0
    }

    def __init__(self):
        self.ITEMS = DataManager("data/item/items.p")
        self.BASE_ITEMS = DataManager("data/item/base_items.p")
        self.RARE_ATTRIBUTES = DataManager(
            "data/item/attributes/rare_attributes.p")
        self.LEGENDARY_ATTRIBUTES = DataManager(
            "data/item/attributes/legendary_attributes.p")
        self.UNIQUE_ATTRIBUTES = DataManager(
            "data/item/attributes/unique_attributes.p")

    def get_item(self, name):
        """Convenience function for getting an item by name"""
        if self.base_items().get(name):
            item = self.base_items()[name]
        else:
            item = self.items()[name]
        return item

    def is_base(self, name):
        """Returns if item is a base item or not"""
        if self.base_items().get(name):
            return True
        return False

    def set_rare_attributes(self, attributes):
        self.RARE_ATTRIBUTES.set(attribtes)

    def set_legendary_attributes(self, attributes):
        self.LEGENDARY_ATTRIBUTES.set(attribtes)

    def set_unique_attributes(self, attributes):
        self.UNIQUE_ATTRIBUTES.set(attribtes)

    def items(self):
        return self.ITEMS.get()

    def base_items(self):
        return self.BASE_ITEMS.get()

    def rare_attributes(self):
        return self.RARE_ATTRIBUTES.get()

    def legendary_attributes(self):
        return self.LEGENDARY_ATTRIBUTES.get()

    def unique_attributes(self):
        return self.UNIQUE_ATTRIBUTES.get()

    def new_item(self, name):
        """Create an empty item object"""
        item = Item(name, self.DEFAULT_ITEM_TYPE,
            dict(self.DEFAULT_ITEM_STATS))
        if self.is_base(name):
            self.base_items()[name] = item
        else:
            self.items()[name] = item

    def delete_item(self, name):
        """Delete attribute by name"""
        if self.is_base(name):
            del self.base_items()[name]
        else:
            del self.items()[name]

    def update_item_stat(self, name, stype, value):
        """Update the item stat"""
        if self.is_base(name):
            self.base_items()[name].stats[stype] = value
        else:
            self.items()[name].stats[stype] = value

    def update_item_type(self, name, itype):
        """Update the item type"""
        if self.is_base(name):
            self.base_items()[name].itype = itype
        else:
            self.items()[name].itype = itype

    def update_item_slot(self, name, slot):
        """Update the item slot"""
        if self.is_base(name):
            self.base_items()[name].slot = slot
        else:
            self.items()[name].slot = slot

    def update_item_name(self, name, new_name):
        """Update the item name"""
        if self.is_base(name):
            item = self.base_items()[name]
            del self.base_items()[name]
            item.name = new_name
            self.base_items()[new_name] = item
        else:
            item = self.items()[name]
            del self.items()[name]
            item.name = new_name
            self.items()[new_name] = item

    def set_item_base(self, name, base):
        """Update the item base"""
        if self.is_base(name) and not base:
            item = self.base_items()[name]
            del self.base_items()[name]
            self.items()[name] = item
        elif not self.is_base(name) and base:
            item = self.items()[name]
            del self.items()[name]
            self.base_items()[name] = item

    def add_item_attribute(self, name, attribute):
        self.get_item(name).attributes.append(attribute)

    def remove_item_attribute(self, name, index):
        del self.get_item(name).attributes[index]

    def new_item_attribute(self, attribute, rarity):
        """Insert a new attribute into the proper attributes dictionary"""
        if rarity == "rare":
            self.rare_attributes()[attribute.name] = attribute
        elif rarity == "legendary":
            self.legendary_attributes()[attribute.name] = attribute
        elif rarity == "unique":
            self.unique_attributes()[attribute.name] = attribute
        else:
            logging.warning("Attempted to make an item attribute: Invalid rarity")

    def delete_item_attribute(self, name, rarity):
        """Delete attribute by name and rarity"""
        if rarity == "rare":
            del self.rare_attributes()[name]
        elif rarity == "legendary":
            del self.legendary_attributes()[name]
        elif rarity == "unique":
            del self.unique_attributes()[name]
        else:
            logging.warning("Attempted to delete an item attribute: Invalid rarity")

    def write(self):
        self.ITEMS.write()
        self.BASE_ITEMS.write()
        self.RARE_ATTRIBUTES.write()
        self.LEGENDARY_ATTRIBUTES.write()
        self.UNIQUE_ATTRIBUTES.write()
