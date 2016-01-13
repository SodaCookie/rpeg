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

    def on_cast(self, source, move):
        self.remove()
        return ""

class Stun(Effect):
    """Sets target's speed to 0 in order to stun"""

    def __init__(self, duration):
        super().__init__("stun", duration)

    def on_get_stat(self, value, stat_type):
        if stat_type == "speed":
            return 0

# def DoT(Effect):
#     """Deals damage of time"""

#     def __init__(self, name, duration):
#         super.__init__(name, duration)