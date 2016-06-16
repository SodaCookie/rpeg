import unittest

from engine.serialization.floor import FloorDataManager
from engine.serialization.dmanager import DataManager

class TestFloorDataManager(FloorDataManager):
    """Overloading the constructor to load the test data"""

    def __init__(self):
        self.FLOORS = DataManager("data/floor_test.p")

class TestFloorSerialization(unittest.TestCase):

    def setUp(self):
        self.dm = TestFloorDataManager()

    def test_floors(self):
        self.assertListEqual(self.dm.floors(), ["any", "catacombs"])

    def test_add_floors(self):
        self.dm.add_floor("test")
        self.assertListEqual(self.dm.floors(), ["any", "catacombs", "test"])

    def test_remove_floors(self):
        self.dm.remove_floor("catacombs")
        self.assertListEqual(self.dm.floors(), ["any"])