from engine.game.dungeon.condition import Condition

class HasShard(Condition):

    def __init__(self, race):
        super().__init__()
        self.race = race

    def apply(self, party):
        return party.has_race(self.race)