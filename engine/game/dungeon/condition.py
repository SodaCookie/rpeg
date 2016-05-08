"""Defines the Condition class used by Dialogues"""

class Condition(object):
    """Object used to determine if a choice can be reached given the
    current party status."""

    def __init__(self, function=None):
        """Takes a function to be checked when the associated choice
        is reachable from its parent Dialogue object."""
        self.function = function

    def apply(self, party):
        """Method to be called to determine if a choice is available to
        the current party. If no function is given during construction
        default returns True. Can be overridden by a subclass safely but
        the subclass must take a party and return a bool"""
        if self.function:
            return self.function(party)
        return True