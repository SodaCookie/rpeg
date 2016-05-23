from engine.game.move.component import Component
import random

class RandomEnemyCast(Component):
    """Defines Random Enemy Target for casting a move"""

    def get_targets(self, selected, caster, players, monsters):
        if not isinstance(caster, type(players[0])):
            return [random.choice([player for player in players if \
                not player.fallen])]
        return [random.choice([monster for monster in monsters if \
            not monster.fallen])]