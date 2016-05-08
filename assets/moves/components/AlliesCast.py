from engine.game.move.component import Component

class AlliesCast(Component):
    """Defines Ally Targetting for a move"""
    def get_targets(self, selected, caster, players, monsters):
        if isinstance(caster, type(players[0])):
            return players
        return monsters