from engine.game.move.component import Component
from assets.moves.components.AddChanceEffect import AddChanceEffect

class AddEffect(AddChanceEffect):
    def __init__(self, effect):
        """Applies an effect on given target(s)
        effect -> Effect"""
        super().__init__(effect, 1)

    def on_cast(self, target, caster, players, monsters):
        self.effect.set_caster(caster)
        damage = target.add_effect(self.effect)
        return ""