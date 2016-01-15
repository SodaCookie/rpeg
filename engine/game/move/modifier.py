"""Defines the base class for Modifiers"""

class Modifier(object):
    """Base class used for all modifiers. Modifiers may be applied
    to integer combat actions (ie, healing, damage, etc)"""

    def modify(self, value, target, caster):
        return value