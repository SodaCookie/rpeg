from engine.game.move.component import Component

class SelfCast(Component):
    """Targeting scheme for casting on self only"""

    def get_targets(self, selected, caster, players, monsters):
        return [caster]