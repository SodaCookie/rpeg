from engine.game.effect.effect import Effect

class DoT(Effect):

    def __init__(self, name, value, duration, tick, modifiers=None,
            dtype="true"):
        """Does heal/damage over time, applies modifiers as well
        If no damage type is given, we assume the value is a heal.
        name -> str
        value -> int
        duration -> float
        tick -> float
        modifiers -> list Modifier
        dtype -> str"""
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