""""This module defines the item system"""
class Item(object):
    """This is the base class for all items"""

    DEFAULT_STATS = {
        "attack": 0,
        "defense": 0,
        "magic": 0,
        "speed": 0,
        "health": 0
    }

    def __init__(self):
        """Basic constructor"""
        self.name = ""
        self.stats = DEFAULT_STATS.copy()
        self.ability = None