from engine.game.move.component import Component
from engine.system import Message

class Damage(Component):

    def __init__(self, damage, dtype, modifiers=None):
        """Deal damage to target.
        damage -> int
        dtype -> str
        modifiers -> list Modifier"""
        self.damage = damage
        self.dtype = dtype
        if not modifiers:
            self.modifiers = []
        else:
            self.modifiers = modifiers

    def on_cast(self, target, caster, players, monsters, system):
        """Order IMPORTANT in modifying damage:
        Suggested standard is additions, then multiplications"""
        damage = self.damage
        for mod in self.modifiers:
            damage = mod.modify(damage, target, caster)
        damage = target.deal_damage(caster, damage, self.dtype)
        system.message("animation", Message("battle-message", target, str(damage), (255, 0, 0)))
        return "%s dealt %d %s damage to %s" % \
            (caster.name, damage, self.dtype, target.name)