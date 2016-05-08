from engine.game.move.component import Component

class SelfEffect(Component):
    """Applies self-effect on cast"""
    def __init__(self, effect):
        self.effect = effect

    def on_cast(self, target, caster, players, monsters):
        damage = caster.add_effect(self.effect)
        return ""