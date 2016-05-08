from engine.game.move.component import Component

class AddChanceEffect(Component):
    """Chance to apply effect on target(s)"""
    def __init__(self, effect, chance):
        self.effect = effect
        self.chance = chance

    def on_cast(self, target, caster, players, monsters):
        rand = random.random()
        if rand > self.chance:
            return ""
        else:
            self.effect.set_caster(caster)
            damage = target.add_effect(self.effect)
            return ""