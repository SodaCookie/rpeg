import random
import xml.etree.ElementTree as tree
import copy
import os

from pygame import image, Surface, SRCALPHA, BLEND_RGBA_MULT
from pygame.transform import scale

import engine.game.character.character as character

from engine.game.monster.general_builder import GeneralBuilder

def parse_tags(filename):
    """Takes a filename and returns a list of all possible tags"""
    root = tree.parse(filename).getroot()
    return [tag.attrib["type"] for tag in root.findall("tags/tag")]

def parse_types(filename):
    """Takes a filename and returns a list of all possible monster types"""
    root = tree.parse(filename).getroot()
    return [tag.tag for tag in root.find("types")]

class Monster(character.Character):

    BUILDERS = [GeneralBuilder]

    DATAPATH = os.path.dirname(os.path.realpath(__file__)) + "/data/"
    TAGS = parse_tags(DATAPATH+"monster.xml")
    TYPES = parse_types(DATAPATH+"monster.xml")
    # NAMES = _XML.find("names")
    # IMAGE = _XML.find("image")

    DEFAULT_RANK = {
        "common": 90,
        "elite": 100,
        "boss": -1
    }

    DEFAULT_STATS = {
        "points": 10,
        "attack": 1,
        "defense": 1,
        "magic": 1,
        "speed": 1,
        "health": 1
    }

    def __init__(self, **parameters):
        """Basic Monster constructor"""
        super().__init__("")
        self.builders = [] # construct builders
        for builder in Monster.BUILDERS:
            value = parameters.get(builder.NAME)
            self.builders.append(builder(value))
        self.builders = sorted(self.builders, key=lambda b: b.priority)

        self.tag = self._generate_tag(Monster.TAGS)
        self.rank = self._generate_rank(Monster.DEFAULT_RANK)
        self.type = self._generate_type(Monster.TYPES)
        self.name = self._generate_name(self.tag, self.rank, self.type)
        self.stats = self._generate_stats(Monster.DEFAULT_STATS, self.tag, self.rank, self.type)
        self.abilities = self._generate_abilities(self.tag, self.rank, self.type)
        self.surface = self._generate_surface()
        self.surface = "image/monster/slime1_base.png"
        self.hover = "image/monster/slime1_highlight.png"

    def _generate_tag(self, tags):
        """Generates the possible tag of the monster"""
        possible_tags = list(tags) # copy
        for builder in self.builders:
            possible_tags = builder.build_tags(possible_tags)
        return random.choice(possible_tags)

    def _generate_type(self, types):
        """Generates the possible type of the monster"""
        possible_types = list(types) # copy
        for builder in self.builders:
            possible_types = builder.build_tags(possible_types)
        return random.choice(possible_types)


    def _generate_rank(self, distribution):
        """Generates the rank of the monster randomly based on distribution"""
        rank_distribution = distribution.copy()
        for builder in self.builders:
            rank_distribution = builder.build_rank(rank_distribution)
        roll = random.randint(0, 100)
        if roll <= rank_distribution["common"]:
            return "common"
        elif roll <= rank_distribution["elite"]:
            return "elite"
        elif roll <= rank_distribution["boss"]:
            return "boss"

    def _generate_name(self, tag, rank, type):
        """Generates a template based on rank, and constructs name with filled in template"""
        if rank == "common":
            name_template = {"adj": ""}
        elif rank == "elite":
            name_template = {"noun": ""}
        else:
            name_template = {"pronoun": ""}
        for builder in self.builders:
            name_template = builder.build_name(name_template, tag, rank, type)

        if rank == "common":
            name = name_template["adj"] + " " + type
        elif rank == "elite":
            name = type + " of the " + name_template["noun"]
        else:
            name = name_template["pronoun"]

        return name

    def _generate_stats(self, stats, tag, rank, type):
        """Generates stats based on distribution"""
        raw_stats = stats.copy()
        for builder in self.builders:
            raw_stats = builder.build_stats(raw_stats, tag, rank, type)

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

    def _generate_abilities(self, tag, rank, type):
        """Generates list of monster abilities"""
        abilities = []
        for builder in self.builders:
            abilities = builder.build_abilities(abilities, tag, rank, type)

        return abilities


    def _generate_surface(self):
        pass
        # base = ""
        # mask = ""
        # overlay = ""
        # enhance = ""
        # splash = ""
        # if self.difficulty >= Monster.COMMON:
        #     base = choice(Monster.IMAGE.findall("base/%s"%self.mtype)).text
        #     mask = choice(Monster.IMAGE.findall("mask/%s"%self.mtype)).text
        #     hover = choice(Monster.IMAGE.findall("hover/%s"%self.mtype)).text
        #     overlay = choice(Monster.IMAGE.findall("overlay/%s"%choice(
        #         self.tags).attrib["type"])).text
        # if self.difficulty >= Monster.ELITE:
        #     enhance = choice(Monster.IMAGE.findall("enhance/%s"%choice(
        #         self.tags).attrib["type"])).text
        # if self.difficulty == Monster.BOSS:
        #     splash = choice(Monster.IMAGE.findall("splash/%s"%choice(
        #         self.tags).attrib["type"])).text

        # if base: base = image.load(base).convert_alpha()
        # if mask: mask = image.load(mask).convert_alpha()
        # if hover: hover = image.load(hover).convert_alpha()
        # if overlay: overlay = image.load(overlay).convert_alpha()
        # if enhance: enhance = image.load(enhance).convert_alpha()
        # if splash: splash = image.load(splash).convert_alpha()

        # tmp_surface = Surface(base.get_size(), SRCALPHA)
        # tmp_surface.fill((0, 0, 0, 0))
        # tmp_hover_surface = tmp_surface.copy()
        # self.surface = Surface(base.get_size(), SRCALPHA)
        # self.hover_surface = Surface(base.get_size(), SRCALPHA)
        # self.surface.fill((0, 0, 0, 0))
        # self.hover_surface.fill((0, 0, 0, 0))

        # if base:
        #     tmp_surface.blit(base, (0, 0))
        #     tmp_hover_surface.blit(hover, (0, 0))
        # if mask:
        #     tmp_surface.blit(mask, (0, 0))
        #     tmp_hover_surface.blit(mask, (0, 0))
        # if overlay:
        #     tmp_surface.blit(overlay, (0, 0), special_flags=BLEND_RGBA_MULT)
        #     tmp_hover_surface.blit(overlay, (0, 0), special_flags=BLEND_RGBA_MULT)
        #     tmp_hover_surface.blit(hover, (0, 0))
        # if enhance:
        #     tmp_surface.blit(enhance, (0, 0))
        #     tmp_hover_surface.blit(enhance, (0, 0))
        # if splash:
        #     self.surface.blit(splash, (0, 0))
        #     self.hover_surface.blit(splash, (0, 0))

        # self.surface.blit(tmp_surface, (0, 0))
        # self.hover_surface.blit(tmp_hover_surface, (0, 0))

        # self.surface = scale(self.surface,
        #             (self.surface.get_width()*SCALE,
        #              self.surface.get_height()*SCALE))

        # self.hover_surface = scale(self.hover_surface,
        #             (self.hover_surface.get_width()*SCALE,
        #              self.hover_surface.get_height()*SCALE))


# For testing
if __name__ == "__main__":
    for i in range(10):
        m = Monster()
        print(m.abilities)