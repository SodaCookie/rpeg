import unittest

import engine.serialization.serialization as serial
from engine.serialization.item import ItemDataManager
from engine.serialization.dmanager import DataManager
from engine.game.item.item import Item
from assets.attributes.RaiseStat import RaiseStat

def setup_data():
    ITEMS = {"item": Item("item", ItemDataManager.DEFAULT_ITEM_TYPE, ItemDataManager.DEFAULT_ITEM_STATS)}
    BASE_ITEMS = {"base": Item("base", ItemDataManager.DEFAULT_ITEM_TYPE, ItemDataManager.DEFAULT_ITEM_STATS)}
    RARE_ATTRIBUTES = {"rare": RaiseStat(1, "attack")}
    LEGENDARY_ATTRIBUTES = {"legendary": RaiseStat(1, "attack")}
    UNIQUE_ATTRIBUTES = {"unique": RaiseStat(1, "attack")}
    serial.serialize(ITEMS, "data/items.p")
    serial.serialize(BASE_ITEMS, "data/base_items.p")
    serial.serialize(RARE_ATTRIBUTES, "data/rare_attributes.p")
    serial.serialize(LEGENDARY_ATTRIBUTES, "data/legendary_attributes.p")
    serial.serialize(UNIQUE_ATTRIBUTES, "data/unique_attributes.p")

class TestItemDataManager(ItemDataManager):

    def __init__(self):
        self.ITEMS = DataManager("data/items.p")
        self.BASE_ITEMS = DataManager("data/base_items.p")
        self.RARE_ATTRIBUTES = DataManager(
            "data/rare_attributes.p")
        self.LEGENDARY_ATTRIBUTES = DataManager(
            "data/legendary_attributes.p")
        self.UNIQUE_ATTRIBUTES = DataManager(
            "data/unique_attributes.p")

class TestItemSerialization(unittest.TestCase):

    def setUp(self):
        setup_data()
        self.dm = TestItemDataManager()

    def test_get_item(self):
        self.assertIsNotNone(self.dm.get_item("item"))
        self.assertIsNotNone(self.dm.get_item("base"))
        self.assertDictEqual(self.dm.get_item("item").stats, ItemDataManager.DEFAULT_ITEM_STATS)
