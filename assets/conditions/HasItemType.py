from engine.game.dungeon.condition import Condition

class HasItemType(Condition):

    def __init__(self, wtype):
        """Test if has itemtype
        wtype -> str"""
        super().__init__()
        self.wtype = wtype

    def apply(self, party):
        return party.has_item_type(self.wtype)