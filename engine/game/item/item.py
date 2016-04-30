
class Item(object):
    """This is the base class for all items"""

    def __init__(self, name, itype, stats, slot="", icon=None, rarity="common",
        attributes=None):
        """Item is simply a container of the item definition. Slot is
        the equipment slot the item fits into."""
        self.icon = None
        self.slot = slot # String describing the slot type
        self.name = name
        self.itype = itype
        self.stats = stats
        self.rarity = rarity
        if attributes:
            self.attributes = attributes
        else:
            self.attributes = []
