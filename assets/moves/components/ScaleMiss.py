from engine.game.move.component import Component

class ScaleMiss(Component):

    def __init__(self, scaling, stype):
        """Scales a miss chance based on stat type.
        scaling -> float
        stype -> string"""
        super().__init__()
        self.scaling = scaling
        self.stype = stype

    def get_miss(self, miss, selected, caster, players, monsters):
        return miss + self.scaling * caster.get_stat(self.stype)

