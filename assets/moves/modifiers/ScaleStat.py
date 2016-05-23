from engine.game.move.modifier import Modifier

class ScaleStat(Modifier):

    def __init__(self, scaling, stype):
        """Additively scales value by a percentage of a stat.
        scaling -> int
        stype -> str"""
        self.scaling = scaling
        self.stype = stype

    def modify(self, value, target, caster):
        return value + self.scaling * caster.get_stat(self.stype)