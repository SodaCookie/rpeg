from engine.game.move.modifier import Modifier

class ScaleLevelAdd(Modifier):
    """Additively scales value by a percentage"""

    def __init__(self, scaling):
        self.scaling = scaling

    def modify(self, value, target, caster):
        return value + self.scaling * caster.get_level()
