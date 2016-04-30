from engine.game.move.component import Component

class Damage(Component):
    """Deals flat damage to given targets"""
    def __init__(self, damage, dtype, modifiers=None):
        self.damage = damage
        self.dtype = dtype
        if not modifiers:
            self.modifiers = []
        else:
            self.modifiers = modifiers

    def on_cast(self, target, caster, players, monsters):
        """Order IMPORTANT in modifying damage:
        Suggested standard is additions, then multiplications"""
        damage = self.damage
        for mod in self.modifiers:
            damage = mod.modify(damage, target, caster)
        damage = target.deal_damage(caster, damage, self.dtype)
        return "%s dealt %d %s damage to %s" % \
            (caster.name, damage, self.dtype, target.name)