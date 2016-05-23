from engine.game.dungeon.condition import Condition

class HasRace(Condition):

    def __init__(self, race):
        """Test if party has a race.
        race -> str"""
        super().__init__()
        self.race = race

    def apply(self, party):
        return party.has_race(self.race)