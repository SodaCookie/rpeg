from engine.game.move.component import Component
from assets.moves.components.AddChanceEffect import AddChanceEffect

class AddEffect(AddChanceEffect):
    """Applies an effect of target(s)"""
    def __init__(self, effect):
        super().__init__(effect, 1)

    def on_cast(self, target, caster, players, monsters):
        self.effect.set_caster(caster)
        damage = target.add_effect(self.effect)
        return ""