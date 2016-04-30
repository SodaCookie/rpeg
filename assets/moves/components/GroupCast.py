from engine.game.move.component import Component

class GroupCast(Component):
    """Defines Group Targetting for a move"""
    def get_targets(self, selected, caster, players, monsters):
        if isinstance(selected[0], type(players[0])):
            return players
        return monsters