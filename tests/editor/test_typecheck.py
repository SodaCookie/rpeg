from editor.meta.typecheck import _get_type
from editor.meta.types import *
import unittest

class TestGetType(unittest.TestCase):

    def test_unknown(self):
        self.assertEqual(type(_get_type("unknown")), UnknownType)

    def test_int(self):
        self.assertEqual(type(_get_type("int")), IntType)

    def test_float(self):
        self.assertEqual(type(_get_type("float")), FloatType)

    def test_str(self):
        self.assertEqual(type(_get_type("str")), StrType)

    def test_list_no_type(self):
        t = _get_type("list")
        self.assertEqual(type(t), ListType)
        self.assertEqual(type(t.elemtype), UnknownType)

    def test_list_no_type_spaces(self):
        t = _get_type("list  ")
        self.assertEqual(type(t), ListType)
        self.assertEqual(type(t.elemtype), UnknownType)

    def test_list_simple(self):
        t = _get_type("list int")
        self.assertEqual(type(t), ListType)
        self.assertEqual(type(t.elemtype), IntType)

    def test_list_compound(self):
        t = _get_type("list list int")
        self.assertEqual(type(t), ListType)
        self.assertEqual(type(t.elemtype), ListType)
        self.assertEqual(type(t.elemtype.elemtype), IntType)

    def test_component(self):
        self.assertEqual(type(_get_type("Component")), ComponentType)

    def test_effect(self):
        self.assertEqual(type(_get_type("Effect")), EffectType)

    def test_modifier(self):
        self.assertEqual(type(_get_type("Modifier")), ModifierType)

    def test_attribute(self):
        self.assertEqual(type(_get_type("Attribute")), AttributeType)

    def test_lambda_simple(self):
        t = _get_type("lambda()")
        self.assertEqual(type(t), LambdaType)
        self.assertEqual(t.args, ())

    def test_lambda_single(self):
        t = _get_type("lambda(test)")
        self.assertEqual(type(t), LambdaType)
        self.assertEqual(t.args, ("test",))

    def test_lambda_multi(self):
        t = _get_type("lambda(test, test2,test3)")
        self.assertEqual(type(t), LambdaType)
        self.assertEqual(t.args, ("test", "test2", "test3"))