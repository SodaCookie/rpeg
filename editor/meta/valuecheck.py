"""Defines functions useful for deriving parameter values in
existing object values"""

import inspect
import re
import logging

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