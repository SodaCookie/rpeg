import random
import xml.etree.ElementTree as tree
import copy
import os

from pygame import image, Surface, SRCALPHA, BLEND_RGBA_MULT
from pygame.transform import scale

import engine.game.character.character as character
from engine.serialization.serialization import deserialize

MOVES = deserialize("data/moves.p")

class Monster(character.Character):
    """The enemy characters encountered in battle. The Monster object
    is responsible for holding a Monster's stats as well as generating
    itself."""

    MONSTERS = deserialize("data/monster.p")

    def __init__(self, name):
        """Basic Monster constructor"""
        super().__init__(name)
        monster_def = Monster.MONSTERS[name] # grab definition

        self.name = name
        self.active_moves = [] # Used to determine the next move
        self.location = monster_def["location"]
        self.graphic = monster_def["graphic"].copy()
        self.rating = monster_def["rating"]
        self.stats.update(monster_def["stats"])
        self.current_health = self.stats["health"]

        # add moves
        for movename in monster_def["abilities"]:
            self.add_move(MOVES[movename])
        self.set_active_moves(self.moves)

        for attribute in monster_def["attributes"]:
            #self.add_effect()
            pass

    def set_active_moves(self, moves):
        self.active_moves = list(moves)

    def handle_battle(self, delta, game, system):
        super().handle_battle(delta, game, system)
        if self.ready:
            if self.active_moves:
                self.selected_move = random.choice(self.active_moves)


# For testing
if __name__ == "__main__":
    for i in range(10):
        m = Monster()
        print(m.abilities)
