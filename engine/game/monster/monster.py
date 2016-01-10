import random
import xml.etree.ElementTree as tree
import copy
import os

from pygame import image, Surface, SRCALPHA, BLEND_RGBA_MULT
from pygame.transform import scale

import engine.game.character.character as character


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
        monsters[name]['rating'] = int(monster.find('rating').text)
    return monsters

class Monster(character.Character):
    """The enemy characters encountered in battle. The Monster object
    is responsible for holding a Monster's stats as well as generating
    itself."""

    DATAPATH = os.path.dirname(os.path.realpath(__file__)) + "/data/"
    MONSTERS = parse_monsters(DATAPATH+"monster.xml")
    # NAMES = _XML.find("names")
    # IMAGE = _XML.find("image")

    def __init__(self, name):
        """Basic Monster constructor"""
        super().__init__("")

# For testing
if __name__ == "__main__":
    for i in range(10):
        m = Monster()
        print(m.abilities)