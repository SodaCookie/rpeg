"""Defines the base class for Component"""

def annotate(*types):
    """Decorator function used to annotate """
    def apply_types(function):
        """Applies a _editor_types field on to the function object"""
        function._editor_types = types
        return function
    return apply_types

class Component(object):
    """Base Class of All component objects. Describes methods
    that are used in move components"""

    def get_targets(self, selected, caster, players, monsters):
        """Get target returns a list of targets in the form of
        character objects, this list is formed from 'selected' targets'
        for instance even though a character's target is a single enemy
        get target will return a full list of enemies since its a
        'Group' component"""
        return []

    def get_miss(self, miss, selected, caster, players, monsters):
        """Returns the miss bound of the move"""
        return miss

    def get_crit(self, crit, selected, caster, players, monsters):
        """Returns the crit bound of the move"""
        return crit

    def on_cast(self, target, caster, players, monsters):
        """Cast of the component move and returns a log
        with a message from that component"""
        return ""

    def valid_target(self, selected, caster, players, monsters):
        """Returns a if the given targets are valid to add to the move"""
        return True

    def valid_cast(self, targets, caster, players, monsters):
        """Returns if a move is ready to be cast"""
        return True