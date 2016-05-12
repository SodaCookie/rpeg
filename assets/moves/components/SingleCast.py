from engine.game.move.component import Component

class SingleCast(Component):
    """Defines Single Targetting for a move"""
    def get_targets(self, selected, caster, players, monsters):
        return selected
