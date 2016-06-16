from engine.game.move.component import Component

class Heal(Component):
    def __init__(self, heal, modifiers):
        """Provides healing for a target.
        heal -> int
        modifiers -> list Modifier"""

        self.heal = heal
        if not modifiers:
            self.modifiers = []
        else:
            self.modifiers = modifiers

    def on_cast(self, target, caster, players, monsters, system):
        """Order IMPORTANT in modifying heal:
        Suggested standard is additions, then multiplications"""
        heal = self.heal
        for mod in self.modifiers:
            heal = mod.modify(heal, target, caster)
        heal = target.apply_heal(caster, heal)
        return "%s healed %s for %d health" % \
            (caster.name, target.name, heal)