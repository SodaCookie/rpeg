from engine.game.move.component import Component

class EnemiesCast(Component):
    """Returns a list of all enemies against the caster"""

    def get_targets(self, selected, caster, players, monsters):
        if isinstance(caster, type(players[0])):
            return monsters
        return players