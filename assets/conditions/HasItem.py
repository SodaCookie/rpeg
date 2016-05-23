from engine.game.dungeon.condition import Condition

class HasItem(Condition):

    def __init__(self, item):
        """Test if has item name
        item -> str"""
        super().__init__()
        self.item = item

    def apply(self, party):
        return party.has_item(self.item)