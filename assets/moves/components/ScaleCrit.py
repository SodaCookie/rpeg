from engine.game.move.component import Component

class ScaleCrit(Component):

    def __init__(self, scaling, stype):
        """Scales a critical chance based on stat type.
        scaling -> float
        stype -> string"""
        super().__init__()
        self.scaling = scaling
        self.stype = stype

    def get_crit(self, crit, selected, caster, players, monsters):
        return crit - self.scaling * caster.get_stat(self.stype)