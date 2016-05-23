from engine.game.move.modifier import Modifier

class ScaleLevelAdd(Modifier):

    def __init__(self, scaling):
        """Additively scales value by a percentage.
        scaling -> float"""
        self.scaling = scaling

    def modify(self, value, target, caster):
        return value + self.scaling * caster.get_level()
