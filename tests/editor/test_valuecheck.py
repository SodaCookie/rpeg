from editor.meta.valuecheck import valuecheck
import unittest

class MockSimple:

    def __init__(self, value):
        self.value = value

class MockComplex:

    def __init__(self, value):
        self.test = value

class TestGetType(unittest.TestCase):

    def test_direct(self):
        mock = MockSimple(5)
        self.assertEqual(valuecheck(mock, "value"), 5)

    def test_indirect(self):
        mock = MockComplex(5)
        self.assertEqual(valuecheck(mock, "value"), 5)

    def test_nofind(self):
        mock = MockComplex(5)
        self.assertEqual(valuecheck(mock, "not_found"), None)