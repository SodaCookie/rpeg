"""Compilation of built effects for the game"""

from engine.game.effect.effect import Effect

class StatChange(Effect):
    """Creates a stat-change with a name, strength, stat to effect and
        duration"""

    def __init__(self, name, strength, stype, duration):
        super().__init__(name, duration)
        self.strength = strength
        self.stype = stype

    def on_get_stat(self, value, stat_type):
        if stat_type == self.stype:
            return value + self.strength
        return value

class StatChangeTilMove(Effect):
    """Creates a stat-change with a name, strength, stat to effect that
    lasts till the next action"""

    def __init__(self, name, strength, stype):
        super().__init__(name, Effect.PERMANENT)
        self.strength = strength
        self.stype = stype

    def on_get_stat(self, value, stat_type):
        if stat_type == self.stype:
            return value + self.strength
        return value

    def on_cast(self, source, move):
        self.remove()
        return ""

class Stun(Effect):
    """Sets target's speed to 0 in order to stun"""

    def __init__(self, duration):
        super().__init__("stun", duration)

    def on_build_action(self, action):
        return 0

class DoT(Effect):
    """Does heal/damage over time, applies modifiers as well
    If no damage type is given, we assume the value is a heal"""

    def __init__(self, name, value, duration, tick, modifiers=None,
        dtype=None):
        super().__init__(name, duration, tick)
        self.value = value
        if modifiers:
            self.modifiers = modifiers
            if self.caster:
                for mod in self.modifiers:
                    value = mod.modify(self.value, self.caster)
        else:
            self.modifiers = []
        self.dtype = dtype

    def on_tick(self):
        if self.owner and self.dtype:
            self.owner.deal_damage(self.owner, self.value, self.dtype)
        elif self.owner:
            self.owner.apply_heal(self.owner, self.value)
        else:
            return "Effect has no owner"