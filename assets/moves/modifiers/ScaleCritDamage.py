from engine.game.move.modifier import Modifier

class ScaleCritDamage(Modifier):

    def __init__(self, scaling):
        """Multiplicatively scales value by a percentage.
        scaling -> float"""
        self.scaling = scaling

    def modify(self, value, target, caster):
        return value * self.scaling
