"""Defines the types used to typecheck the docstrings of assets"""
from types import LambdaType

from engine.game.move.component import Component
from engine.game.move.modifier import Modifier
from engine.game.effect.effect import Effect
from engine.game.attribute.attribute import Attribute

__all__ = ["UnknownType", "IntType", "FloatType", "StrType", "ListType",
    "ComponentType", "EffectType", "ModifierType", "AttributeType",
    "LambdaType"]

class EditorType:
    """Defines base type required for editor to use"""

    def __init__(self, basetype):
        self.basetype = basetype # Actual python type


class UnknownType(EditorType):
    """Defines the type required for unknown type"""

    def __init__(self):
        super().__init__(None)

    def __str__(self):
        return "unknown"


class IntType(EditorType):
    """Defines the type required for int type"""

    def __init__(self):
        super().__init__(int)

    def __str__(self):
        return "int"


class FloatType(EditorType):
    """Defines the type required for float type"""

    def __init__(self):
        super().__init__(float)

    def __str__(self):
        return "float"


class StrType(EditorType):
    """Defines the type required for str type"""

    def __init__(self):
        super().__init__(str)

    def __str__(self):
        return "str"


class ListType(EditorType):
    """Defines the type required for list type"""

    def __init__(self, elemtype):
        """Creates a new ListType with element type as an EditorType"""
        super().__init__(list)
        self.elemtype = elemtype

    def __str__(self):
        return "list " + str(self.elemtype)


class ComponentType(EditorType):
    """Defines the type required for Component type"""

    def __init__(self):
        super().__init__(Component)

    def __str__(self):
        return "Component"


class EffectType(EditorType):
    """Defines the type required for Effect type"""

    def __init__(self):
        super().__init__(Effect)

    def __str__(self):
        return "Effect"


class ModifierType(EditorType):
    """Defines the type required for Modifier type"""

    def __init__(self):
        super().__init__(Modifier)

    def __str__(self):
        return "Modifier"


class AttributeType(EditorType):
    """Defines the type required for Attribute type"""

    def __init__(self):
        super().__init__(Attribute)

    def __str__(self):
        return "Attribute"


class LambdaType(EditorType):
    """Defines the type required for lambda type"""

    def __init__(self, *args):
        """Creates a new LambdaType with parameters as strings"""
        super().__init__(LambdaType)
        self.args = args

    def __str__(self):
        return "lambda (%s)" % ", ".join(self.args)