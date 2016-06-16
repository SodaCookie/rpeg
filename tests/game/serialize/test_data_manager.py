import unittest

from engine.serialization.dmanager import DataManager

class TestObject():
    def __init__(self, val):
        self.val = val

class TestDataManager(unittest.TestCase):

    def setUp(self):
        self.filename = "data/data_test.p"
        self.dm = DataManager(self.filename)

    def test_get(self):
        """Determine if one can get newly set data"""
        test_obj = TestObject("test")
        self.dm.set(test_obj)
        self.assertEqual(self.dm.get().val, test_obj.val)

    def test_reference(self):
        """Determine if the reference is the same"""
        dm2 = DataManager(self.filename)
        self.assertIs(self.dm.get(), dm2.get())

    def test_write(self):
        """Determine if other DataManagers can get written data"""
        dm2 = DataManager(self.filename)
        test_obj = TestObject("test")
        self.dm.set(test_obj)
        self.dm.write()
        self.assertEqual(dm2.get().val, test_obj.val)
        self.assertIs(self.dm.get(), dm2.get())

    def test_del_reference(self):
        dm2 = DataManager(self.filename)
        self.assertEqual(len(DataManager.cache), 1)
        del dm2
        self.assertEqual(len(DataManager.cache), 1)
        del self.dm
        self.assertEqual(len(DataManager.cache), 0)
