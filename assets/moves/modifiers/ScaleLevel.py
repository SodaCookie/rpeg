from engine.game.move.modifier import Modifier

class ScaleLevel(Modifier):
    """Multiplicatively scales value by a percentage of level"""

    def __init__(self, scaling):
        self.scaling = scaling

    def modify(self, value, target, caster):
        return value * (self.scaling * caster.get_level())
