from engine.game.move.component import Component

class AlliesOnly(Component):
    """Descriptor for targetting allies only"""
    def valid_target(self, selected, caster, players, monsters):
        return all([isinstance(t, type(caster)) for t in selected])