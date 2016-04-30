from engine.game.move.modifier import Modifier

class ScaleCritDamage(Modifier):
    """Multiplicatively scales value by a percentage"""

    def __init__(self, scaling):
        self.scaling = scaling

    def modify(self, value, target, caster):
        return value * self.scaling
