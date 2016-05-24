"""Defines functions useful for deriving parameter values in
existing object values"""
import inspect
import logging
import re
from types import LambdaType as _LambdaType

from engine.game.move.component import Component
from engine.game.move.modifier import Modifier
from engine.game.effect.effect import Effect
from engine.game.attribute.attribute import Attribute
from editor.meta.types import *

_assign_regex = r"self\.(\w+)\s*=\s*(?:%s)"

def valuecheck(obj, parameter):
    """Attempts to return the value of a parameter.
    Returns None if no value can be found"""
    if hasattr(obj, parameter):
        """Basic search"""
        return getattr(obj, parameter)
    elif hasattr(obj, "__init__"):
        try:
            source = inspect.getsource(obj.__init__)
            match = re.search(_assign_regex % parameter, source)
            if match:
                member = match.group(1)
                return getattr(obj, member)
        except OSError:
            print("Source file for %s could not be found." % obj)
            logging.info("Source file for %s could not be found." % obj)
        except AttributeError:
            logging.error("Pickled object has been updated and %s could not be found" % member)
    return None

def value_from_type(value):
    """Given a value attempt to return the EditorType"""
    if isinstance(value, int):
        return IntType()
    elif isinstance(value, float):
        return FloatType()
    elif isinstance(value, str):
        return StrType()
    elif isinstance(value, list):
        if len(value) > 0:
            return ListType(value_from_type(value[0]))
        else:
            return ListType(UnknownType())
    elif isinstance(value, Component):
        return ComponentType()
    elif isinstance(value, Effect):
        return EffectType()
    elif isinstance(value, Modifier):
        return ModifierType()
    elif isinstance(value, Attribute):
        return AttributeType()
    elif isinstance(value, _LambdaType):
        args = [p for p in inspect.signature(value).parameters]
        return LambdaType(*args)
    else:
        return UnknownType()
