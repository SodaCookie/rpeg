from engine.game.move.component import Component

class SingleCast(Component):
    """Defines Single Targeting for a move"""

    def get_targets(self, selected, caster, players, monsters):
        return selected
