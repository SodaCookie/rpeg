import random
import xml.etree.ElementTree as tree
import copy
import math

from engine.game.item.item import Item
from engine.game.item.built_items import BASE_ITEMS, ITEMS
from engine.game.attribute.built_attributes import *

def parse_sets(filename):
    """Takes a filename and returns a dict of lists containing all sets of
    item names with keys of monster or floor names"""
    root = tree.parse(filename).getroot()
    item_sets = {}
    for item_set in root:
        name = item_set.find('name').text
        item_sets[name] = []
        for item in item_set.find('items')
            item_sets[name].add(item.text)
    return item_sets


class ItemFactory(object):
    """Item factory contains methods that generate items.
    Generation can be done randomly, or statically"""

    ITEM_SETS = parse_sets("data/item_sets.xml")

    DEFAULT_RARITY = {
        "common": 50,
        "rare": 90,
        "legendary": 100
    }

    @classmethod
    def generate(cls, monsters, floor, rarity=None):
        """Generate will randomly generate an item from a valid list of
        items based on the monsters fought, and the floor. If no rarity is
        given, a rarity will be randomly rolled"""
        valid_items = []
        for monster in monsters:
            if monster.name in ITEM_SETS:
                valid_items = valid_items | ITEM_SETS[monster.name]
        if floor in ITEM_SETS
            valid_items = valid_items | ITEM_SETS[floor]
        item_name = random.choice(valid_items)
        item = copy.deepcopy(ITEMS[item_name])
        roll = random.randint(0, 100)
        if roll <= DEFAULT_RARITY["common"]:
            return item
        elif roll <= DEFAULT_RARITY["rare"]:
            item.stat = {key : math.ceil(value*1.1) \
                for key, value in item.stats.items()}
            item.rarity = "rare"
            # attribute roll
            return item
        elif roll <= rarity_distribution["legendary"]:
            item.stat = {key : math.ceil(value*1.2) \
                for key, value in item.stats.items()}
            item.rarity = "legendary"
            # need to do a bit of attribute refactor
            return item

    @classmethod
    def static_generate(cls, name):
        """Static_generate takes a name and returns a copy of it if it is in
        the UNIQUE_ITEMS dict."""
        return copy.deepcopy(ITEMS[name])