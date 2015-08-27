""""This module defines the item system"""
import os
import re
import random
import copy
from xml.etree import ElementTree

from engine.game.item.general_builder import GeneralBuilder
from engine.game.item.rarity_builder import RarityBuilder
from engine.game.item.floor_builder import FloorBuilder

__all__ = ["Item"]

def parse_tags(filename):
    """Take a filename to an xml file and return a list of possible
    tags for rolling."""
    root = ElementTree.parse(filename).getroot()
    return [child.tag for child in root]

def parse_types(filename):
    """Take a filename to an xml file and return a dictionary of
    a type to dictionary of stats."""
    root = ElementTree.parse(filename).getroot()
    types = {}
    for itemtype in root:
        types[itemtype.attrib['name']] = {}
        for stat in itemtype:
            key, value = stat.tag, stat.text
            if re.match("^-?[\d\.]+$", value): # is a numeric
                value = float(value)
            types[itemtype.attrib['name']][key] = value
    return types

def parse_templates(filename):
    """Take a filename to an xml file and returns a dictionary of
    rarities to all the templates in each rarity."""
    root = ElementTree.parse(filename).getroot()
    templates = {}
    for rarity in ["common", "rare", "epic", "legendary"]:
        templates[rarity] = root.findall("template[@rarity='%s']"%rarity)
        templates[rarity] = [node.text for node in templates[rarity]]
    return templates

class Item(object):
    """This is the base class for all items"""

    DEFAULT_STATS = {
        "points": 10,
        "attack": 1,
        "defense": 1,
        "magic": 1,
        "speed": 1,
        "health": 1
    }

    DEFAULT_RARITY = {
        "common": 65,
        "rare": 85,
        "epic": 95,
        "legendary": 100
    }

    BUILDERS = [GeneralBuilder, RarityBuilder, FloorBuilder]
    DATA_PATH = os.path.dirname(os.path.realpath(__file__)) + "/data/"
    TAGS = parse_tags(DATA_PATH+'tags.xml')
    TYPES = parse_types(DATA_PATH+'types.xml')
    TEMPLATES = parse_templates(DATA_PATH+'templates.xml')

    def __init__(self, **parameters):
        """Basic constructor if no parameter for the builder is specified
        than None will be passed"""
        self.builders = [] # construct builders
        for builder in Item.BUILDERS:
            value = parameters.get(builder.NAME)
            self.builders.append(builder(value))
        self.builders = sorted(self.builders, key=lambda b: b.priority)

        self.tag = self._generate_tag(Item.TAGS)
        self.rarity = self._generate_rarity(Item.DEFAULT_RARITY)
        self.template = self._generate_template(Item.TEMPLATES, self.rarity)
        self.type = self._generate_type(Item.TYPES)
        self.name = self._generate_name(self.template, self.tag, self.rarity)
        self.stats = self._generate_stats(Item.DEFAULT_STATS, self.tag, self.rarity, self.type)
        self.abilities = self._generate_abilities() # to be completed when the abilities are good

    def _generate_tag(self, tags):
        """Generates the possible tag of the item"""
        possible_tags = list(tags) # copy
        for builder in self.builders:
            possible_tags = builder.build_tags(possible_tags)
        return random.choice(possible_tags)

    def _generate_rarity(self, distribution):
        """Generates the rarity of the item"""
        rarity_distribution = distribution.copy()
        for builder in self.builders:
            rarity_distribution = builder.build_rarity(rarity_distribution)
        roll = random.randint(0, 100)
        if roll <= rarity_distribution["common"]:
            return "common"
        elif roll <= rarity_distribution["rare"]:
            return "rare"
        elif roll <= rarity_distribution["epic"]:
            return "epic"
        elif roll <= rarity_distribution["legendary"]:
            return "legendary"

    def _generate_template(self, templates, rarity):
        """Generates the specific name of the template"""
        return random.choice(templates[rarity])

    def _generate_type(self, types):
        """Generates the type of item that the item will be"""
        possible_types = copy.deepcopy(types)
        for builder in self.builders:
            possible_types = builder.build_types(possible_types)
        return random.choice(list(possible_types.items()))

    def _generate_name(self, template, tag, rarity):
        """Converts template string into hash of tuple (count, type) to
        a list of strings. Then it passes to the builders to build the
        name"""
        keys = {}
        template = template.replace("[item]", self.type[0]) # self.type is a tuple, because .items
        for match in re.finditer("\[(.+?)\]", template):
            if keys.get(match.group(1)) == None:
                keys[match.group(1)] = 0
            keys[match.group(1)] += 1

        conv_template = {(key, count): ["" for i in range(count)]
            for key, count in keys.items()} # convert to type

        for builder in self.builders:
            conv_template = builder.build_name(conv_template, tag, rarity)

        for key, words in conv_template.items():
            speech, count = key
            for i in range(count):
                template = template.replace("[%s]"%speech, words[i], 1)
        return template.title()

    def _generate_stats(self, stats, tag, rarity, type):
        raw_stats = stats.copy()
        for builder in self.builders:
            raw_stats = builder.build_stats(raw_stats, tag, rarity, type)

        s =   raw_stats["attack"]\
            + raw_stats["defense"]\
            + raw_stats["magic"]\
            + raw_stats["speed"]\
            + raw_stats["health"]
        attack_dist = raw_stats["attack"] / s
        defense_dist = raw_stats["defense"] / s
        magic_dist = raw_stats["magic"] / s
        speed_dist = raw_stats["speed"] / s
        health_dist = raw_stats["health"] / s

        stats = {}
        stats["points"] = round(raw_stats["points"])
        stats["attack"] = round(raw_stats["points"] * attack_dist)
        stats["defense"] = round(raw_stats["points"] * defense_dist)
        stats["magic"] = round(raw_stats["points"] * magic_dist)
        stats["speed"] = round(raw_stats["points"] * speed_dist)
        stats["health"] = round(raw_stats["points"] * health_dist)

        return stats

    def _generate_abilities(self):
        """TBC"""
        return []

    def __hash__(self):
        return self.name.__hash__()


if __name__ == "__main__":
    # print("TAGS:" ,Item.TAGS)
    # print("TEMPLATES:" ,Item.TEMPLATES)
    # print("TYPES:" , Item.TYPES)
    for i in range(10):
        i = Item(rarity="legendary", floor=5)
        print(i.rarity, i.stats)