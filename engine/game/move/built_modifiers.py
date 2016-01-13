"""Compilation of the modifiers to be applied to move values"""

from engine.game.move.modifier import Modifier
import engine.game.player.player as Player


class ScaleStat(Modifier):
    """Additively scales value by a percentage of a stat"""

    def __init__(self, scaling, stype):
        self.scaling = scaling
        self.stype = stype

    def modify(self, value, target, caster, players, monsters):
        return value + self.scaling * caster.get_stat(self.stype)

class ScaleLevel(Modifier):
    """Multiplicatively scales value by a percentage of level"""

    def __init__(self, scaling):
        self.scaling = scaling

    def modify(self, value, target, caster, players, monsters):
        return value * (self.scaling * caster.get_level())

class ScaleCrit(Modifier):
    """Multiplicatively scales value by a percentage"""

    def __init__(self, scaling):
        self.scaling = scaling

    def modify(self, value, target, caster, players, monsters):
        return value * self.scaling