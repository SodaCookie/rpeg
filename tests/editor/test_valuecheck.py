from editor.meta.valuecheck import valuecheck, value_from_type
from editor.meta.types import *
from engine.game.move.component import Component
from engine.game.move.modifier import Modifier
from engine.game.effect.effect import Effect
from engine.game.attribute.attribute import Attribute

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


class TestFromValue(unittest.TestCase):

    def test_int(self):
        self.assertEqual(type(value_from_type(1)), IntType)

    def test_float(self):
        self.assertEqual(type(value_from_type(1.0)), FloatType)

    def test_str(self):
        self.assertEqual(type(value_from_type("Hello")), StrType)

    def test_list_simple(self):
        t = value_from_type([])
        self.assertEqual(type(t), ListType)
        self.assertEqual(type(t.elemtype), UnknownType)

    def test_list_simple_typed(self):
        t = value_from_type([1, 2, 3])
        self.assertEqual(type(t), ListType)
        self.assertEqual(type(t.elemtype), IntType)

    def test_list_custom_typed(self):
        t = value_from_type([Component()])
        self.assertEqual(type(t), ListType)
        self.assertEqual(type(t.elemtype), ComponentType)

    def test_list_complex_type(self):
        t = value_from_type([[1], [2], [3]])
        self.assertEqual(type(t), ListType)
        self.assertEqual(type(t.elemtype), ListType)
        self.assertEqual(type(t.elemtype.elemtype), IntType)

    def test_component(self):
        self.assertEqual(type(value_from_type(Component())), ComponentType)

    def test_effect(self):
        self.assertEqual(
            type(value_from_type(Effect("test", 1.0))), EffectType)

    def test_modifier(self):
        self.assertEqual(type(value_from_type(Modifier())), ModifierType)

    def test_attribute(self):
        self.assertEqual(type(value_from_type(Attribute("test"))), AttributeType)

    def test_lambda_simple(self):
        self.assertEqual(type(value_from_type(lambda : print("hello"))),
            LambdaType)

    def test_lambda_sig(self):
        t = value_from_type(lambda x: print(x))
        self.assertEqual(type(t), LambdaType)
        self.assertEqual(t.args, ("x",))

    def test_lambda_multi_sig(self):
        t = value_from_type(lambda x, y, z: print(x, y, z))
        self.assertEqual(type(t), LambdaType)
        self.assertEqual(t.args, ("x", "y", "z"))

    def test_unknown(self):
        self.assertEqual(type(value_from_type(object())), UnknownType)