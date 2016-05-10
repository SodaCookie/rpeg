import random
import xml.etree.ElementTree as tree
import copy
import math

from engine.serialization.serialization import deserialize
from engine.game.item.item import Item
from engine.game.item.built_items import BASE_ITEMS, ITEMS
from engine.game.attribute.built_item_attributes import RARE_ATTRIBUTES, \
    LEGENDARY_ATTRIBUTES, UNIQUE_ATTRIBUTES


class ItemFactory(object):
    """Item factory contains methods that generate items.
    Generation can be done randomly, or statically"""

    ITEM_SETS = deserialize("data/item/item_sets.p")

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
            if monster.name in cls.ITEM_SETS:
                valid_items.extend(cls.ITEM_SETS[monster.name])
        if floor in cls.ITEM_SETS:
            valid_items.extend(cls.ITEM_SETS[floor])
        item_name = random.choice(valid_items)
        item = copy.deepcopy(ITEMS[item_name])
        if item.itype == "extra": # extra items must be rare or better
            roll = random.randint(51, 100)
        else:
            roll = random.randint(0, 100)

        # Rolls confirmed
        if roll <= cls.DEFAULT_RARITY["common"]:
            item.name = item.name.title()
        elif roll <= cls.DEFAULT_RARITY["rare"]:
            # Roll for rare, one attribute (one rare)
            # 10% increased stats
            item.stat = {key : math.ceil(value*1.1) \
                for key, value in item.stats.items()}
            item.rarity = "rare"
            desc, attribute = copy.deepcopy(random.choice(
                list(RARE_ATTRIBUTES.items())))
            # Rename
            item.attributes.append(attribute)
            item.name = "%s %s" % (desc, item.name)
            item.name = item.name.title()
        elif roll <= cls.DEFAULT_RARITY["legendary"]:
            # Roll for legendary, two attributes (one rare and one legend)
            # 20% increased stats
            item.stat = {key : math.ceil(value*1.2) \
                for key, value in item.stats.items()}
            item.rarity = "legendary"
            _, attribute = copy.deepcopy(random.choice( # ignore the first attr
                list(RARE_ATTRIBUTES.items())))
            item.attributes.append(attribute)
            desc, attribute = copy.deepcopy(random.choice(
                list(LEGENDARY_ATTRIBUTES.items())))
            item.attributes.append(attribute)
            item.name = "%s %s" % (desc, item.name)
            item.name = item.name.title()
        return item

    @classmethod
    def static_generate(cls, name):
        """Static_generate takes a name and returns a copy of it if it is in
        the UNIQUE_ITEMS dict."""
        return copy.deepcopy(ITEMS[name])