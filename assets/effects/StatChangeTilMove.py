from engine.game.effect.effect import Effect

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

    def on_refresh(self, effect):
        self.active = True
        self.duration = self.max_duration