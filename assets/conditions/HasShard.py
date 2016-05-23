from engine.game.dungeon.condition import Condition

class HasShard(Condition):

    def __init__(self, shards):
        """Tests if party has a sufficient number of shards.
        shards -> int"""
        super().__init__()
        self.shards = shards

    def apply(self, party):
        return party.has_shards(self.shards)