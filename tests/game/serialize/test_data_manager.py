import unittest
import os

from engine.serialization.dmanager import DataManager

class TestDataManager(unittest.TestCase):

    def setUp(self):
        self.dm = DataManager("tests/game/serialize/data/data_test.p")

    def test_get(self):
        self.assertEqual(self.dm.get().value, "test")

    def test_reference(self):
        """Determine if the reference is the same"""
        dm2 = DataManager("tests/game/serialize/data/data_test.p")
        self.assertIs(self.dm.get(), dm2.get())

    def test_del_reference(self):
        self.assertEqual(len(DataManager.cache), 1)
        del self.dm
        self.assertEqual(len(DataManager.cache), 0)
