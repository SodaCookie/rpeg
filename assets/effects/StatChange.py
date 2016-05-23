from engine.game.effect.effect import Effect

class StatChange(Effect):
    """Creates a stat-change with a name, strength, stat to effect and
        duration"""

    def __init__(self, name, strength, stype, duration):
        """Changes the stats based on stat type additively
        name -> str
        strength -> int
        stype -> str
        duration -> float"""
        super().__init__(name, duration)
        self.strength = strength
        self.stype = stype

    def on_get_stat(self, value, stat_type):
        if stat_type == self.stype:
            return value + self.strength
        return value
