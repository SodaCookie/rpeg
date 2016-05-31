"""Defines the functions import for the editor to typecheck assets"""

import inspect
import re

from editor.meta.types import *

# Regexes
_type_regex = re.compile(r"^\s*\b(\w+)\b\s*->\s*(.+)", re.MULTILINE)
_int_regex = re.compile(r"^\s*\bint\b", re.MULTILINE)
_float_regex = re.compile(r"^\s*\bfloat\b", re.MULTILINE)
_str_regex = re.compile(r"^\s*\b(?:str|string)\b|", re.MULTILINE)
_list_regex = re.compile(r"^\s*\blist\b\s*(.*)", re.MULTILINE)
_component_regex = re.compile(r"^\s*\bComponent\b", re.MULTILINE)
_effect_regex = re.compile(r"^\s*\bEffect\b", re.MULTILINE)
_modifier_regex = re.compile(r"^\s*\bModifier\b", re.MULTILINE)
_attribute_regex = re.compile(r"^\s*\bAttribute\b", re.MULTILINE)
_lambda_regex = re.compile(r"^\s*\blambda\b\s*\((.*)\)", re.MULTILINE)
_parameter_regex = re.compile(r"\b\w+\b")

def _get_type(type_string):
    """Parses the type part of the string and returns the type"""
    if _list_regex.match(type_string):
        elemtype = _list_regex.match(type_string).group(1)
        return ListType(_get_type(elemtype))
    elif _lambda_regex.match(type_string):
        parameter_string = _lambda_regex.match(type_string).group(1)
        return LambdaType(*_parameter_regex.findall(parameter_string))
    elif _int_regex.match(type_string):
        return IntType()
    elif _float_regex.match(type_string):
        return FloatType()
    elif _str_regex.match(type_string):
        return StrType()
    elif _component_regex.match(type_string):
        return ComponentType()
    elif _effect_regex.match(type_string):
        return EffectType()
    elif _modifier_regex.match(type_string):
        return ModifierType()
    elif _attribute_regex.match(type_string):
        return AttributeType()
    else:
        return UnknownType()

def typecheck(cls):
    """By parsing a classes constructor's docstring, determines the types of
    the parameters by the class"""
    docstring = cls.__init__.__doc__
    signature = inspect.signature(cls)
    parsed_parameters = {}
    if docstring:
        for parameter, type_string in re.findall(_type_regex, docstring):
            parsed_parameters[parameter] = _get_type(type_string)

    parameters = {}
    for parameter in signature.parameters.values():
        if parsed_parameters.get(parameter.name):
            parameters[parameter.name] = parsed_parameters[parameter.name]
        else:
            parameters[parameter.name] = UnknownType()
    return parameters
