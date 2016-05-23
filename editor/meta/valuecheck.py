"""Defines functions useful for deriving parameter values in
existing object values"""

import inspect
import re

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
            print("Error")
    return None