from engine.game.move.component import Component

class SelfEffect(Component):

    def __init__(self, effect):
        """Applies self-effect on cast.
        effect -> Effect"""
        self.effect = effect

    def on_cast(self, target, caster, players, monsters):
        damage = caster.add_effect(self.effect)
        return ""