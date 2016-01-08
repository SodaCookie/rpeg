import random
import os

from engine.game.dungeon.rooms.shop.builder import Builder, parse_shopnames
from engine.game.item.item import Item


class GeneralBuilder(Builder):

    DATAPATH = os.path.dirname(os.path.realpath(__file__)) + "/data/"
    NAME = "_general"

    def __init__(self, value):
        super().__init__(0, None)

    def build_items(self, items):
        """Generate 3-5 random items and fill in price based on stats"""
        for i in range(random.randint(3, 4)):
            item = Item()
            value = item.stats["points"]
            items[item] = round(value)
        return items

    def build_name(self, name):
        """Return a random name from our list of shop names"""
        choices = parse_shopnames(GeneralBuilder.DATAPATH+"shop_names")
        return random.choice(choices)