from engine.game.move.component import Component

class EnemiesOnly(Component):
    """Descriptor for targetting enemies only"""
    def valid_target(self, selected, caster, players, monsters):
        return all([not isinstance(t, type(caster)) for t in selected])