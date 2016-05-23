from engine.game.move.component import Component

class AddChanceEffect(Component):

    def __init__(self, effect, chance):
        """Applies an effect with a given percent chance 100 being guaranteed
        effect -> Effect
        chance -> int"""
        self.effect = effect
        self.chance = chance

    def on_cast(self, target, caster, players, monsters):
        rand = random.randint(0, 99)
        if rand > self.chance:
            return ""
        else:
            self.effect.set_caster(caster)
            damage = target.add_effect(self.effect)
            return ""