from engine.game.move.component import Component

class Heal(Component):
    """Deals flat healing to given targets"""
    def __init__(self, heal, modifiers):
        self.heal = heal
        if not modifiers:
            self.modifiers = []
        else:
            self.modifiers = modifiers

    def on_cast(self, target, caster, players, monsters):
        """Order IMPORTANT in modifying heal:
        Suggested standard is additions, then multiplications"""
        heal = self.heal
        for mod in self.modifiers:
            heal = mod.modify(heal, target, caster)
        heal = target.apply_heal(caster, heal)
        return "%s healed %s for %d health" % \
            (caster.name, target.name, heal)