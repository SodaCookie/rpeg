from engine.game.move.modifier import Modifier

class ScaleLevel(Modifier):

    def __init__(self, scaling):
        """Multiplicatively scales value by a percentage of level.
        scaling -> float"""
        self.scaling = scaling

    def modify(self, value, target, caster):
        return value * (self.scaling * caster.get_level())
