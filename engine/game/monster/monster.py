import random
import xml.etree.ElementTree as tree
import copy
import os

from pygame import image, Surface, SRCALPHA, BLEND_RGBA_MULT
from pygame.transform import scale

import engine.game.character.character as character
import engine.game.move.built_moves as built_moves


def parse_monsters(filename):
    """Takes a filename and returns a dict of dicts containing all monster
    definitions with keys of monster names"""
    root = tree.parse(filename).getroot()
    monsters = {}
    for monster in root:
        name = monster.find('name').text
        monsters[name] = {}
        monsters[name]['location'] = monster.find('location').text
        monsters[name]['stats'] = {}
        for stat in monster.find('stats'):
            monsters[name]['stats'][stat.tag] = int(stat.text)
        monsters[name]['abilities'] = []
        for ability in monster.find('abilities'):
            monsters[name]['abilities'].append(ability.text)
        monsters[name]['attributes'] = []
        for attribute in monster.find('attributes'):
            monsters[name]['attributes'].append(attribute.text)
        monsters[name]['graphic'] = {} # we need to do some work here
        for graphic in monster.find('graphics'):
            monsters[name]['graphic'][graphic.attrib["name"]] = graphic.text
        monsters[name]['rating'] = int(monster.find('rating').text)
    return monsters


class Monster(character.Character):
    """The enemy characters encountered in battle. The Monster object
    is responsible for holding a Monster's stats as well as generating
    itself."""

    MONSTERS = parse_monsters("data/monster.xml")

    def __init__(self, name):
        """Basic Monster constructor"""
        super().__init__(name)
        monster_def = Monster.MONSTERS[name] # grab definition

        self.name = name
        self.location = monster_def["location"]
        self.graphic = monster_def["graphic"].copy()
        self.rating = monster_def["rating"]
        self.stats.update(monster_def["stats"])
        # add moves
        # for movename in monster_def["abilities"]:
        #     self.add_move(built_moves.MONSTER_MOVES[movename])
        for attribute in monster_def["attributes"]:
            #self.add_effect()
            pass


# For testing
if __name__ == "__main__":
    for i in range(10):
        m = Monster()
        print(m.abilities)