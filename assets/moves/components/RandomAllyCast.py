from engine.game.move.component import Component
import random

class RandomAllyCast(Component):
    """Defines Random Ally Target for a move"""
    def get_targets(self, selected, caster, players, monsters):
        if isinstance(type(caster), type(players[0])):
            return [random.choice([player for player in players if \
                not player.fallen])]
        return [random.choice([monster for monster in monsters if \
            not monster.fallen])]