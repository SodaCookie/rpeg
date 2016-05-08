from engine.game.move.component import Component

class EnemiesCast(Component):
    """Defines Enemy Targetting for a move"""
    def get_targets(self, selected, caster, players, monsters):
        if isinstance(caster, type(players[0])):
            return monsters
        return players