from engine.game.dungeon.condition import Condition

class HasShard(Condition):

    def __init__(self, wtype):
        super().__init__()
        self.wtype = wtype

    def apply(self, party):
        return party.has_item_type(self.wtype)