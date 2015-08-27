from random import choice, randint
import xml.etree.ElementTree as tree
import copy
import os

from pygame import image, Surface, SRCALPHA, BLEND_RGBA_MULT
from pygame.transform import scale

import classes.game.character as character
from classes.rendering.view import SCALE

def parse_tags(filename):
    """Takes a filename and returns a list of all possible tags"""
    root = tree.parse(filename).getroot()
    return [tag.attrib["type"] for tag in root.findall("tags/tag")]

def parse_types(filename):
    """Takes a filename and returns a list of all possible monster types"""
    root = tree.parse(filename).getroot()
    return [tag.tag for tag in root.find("types")]

class Monster(character.Character):

    BUILDERS = []

    DATAPATH = os.path.dirname(os.path.realpath(__file__)) + "/data/"
    TAGS = parse_tags(DATAPATH+"monsters.xml")
    TYPES = parse_types(DATAPATH+"monsters.xml")
    NAMES = _XML.find("names")
    IMAGE = _XML.find("image")

    def __init__(self, **parameters):
        """Basic Monster constructor"""
        super().__init__("")

        self.builders = [] # construct builders
        for builder in Item.BUILDERS:
            value = parameters.get(builder.NAME)
            self.builders.append(builder(value))
        self.builders = sorted(self.builders, key=lambda b: b.priority)

        self.tag = self._generate_tag(Monster.TAGS)
        self.rank = None
        self.type = None
        self.name = None
        self.stats = None
        self.ablilities = None
        self.surface = None

    def _generate_tag(self, tags):
        """Generates the possible tag of the item"""
        possible_tags = list(tags) # copy
        for builder in self.builders:
            possible_tags = builder.build_tags(possible_tags)
        return random.choice(possible_tags)

    def _generate_stats(self):
        """Generates stats based on the power level of the players"""
        pass

    def _generate_type(self):
        pass

    def _generate_name(self):
        pass

    def _generate_stats(self):
        pass

    def _generate_abilities(self):
        pass

    def generate_surface(self):
        base = ""
        mask = ""
        overlay = ""
        enhance = ""
        splash = ""
        if self.difficulty >= Monster.COMMON:
            base = choice(Monster.IMAGE.findall("base/%s"%self.mtype)).text
            mask = choice(Monster.IMAGE.findall("mask/%s"%self.mtype)).text
            hover = choice(Monster.IMAGE.findall("hover/%s"%self.mtype)).text
            overlay = choice(Monster.IMAGE.findall("overlay/%s"%choice(
                self.tags).attrib["type"])).text
        if self.difficulty >= Monster.ELITE:
            enhance = choice(Monster.IMAGE.findall("enhance/%s"%choice(
                self.tags).attrib["type"])).text
        if self.difficulty == Monster.BOSS:
            splash = choice(Monster.IMAGE.findall("splash/%s"%choice(
                self.tags).attrib["type"])).text

        if base: base = image.load(base).convert_alpha()
        if mask: mask = image.load(mask).convert_alpha()
        if hover: hover = image.load(hover).convert_alpha()
        if overlay: overlay = image.load(overlay).convert_alpha()
        if enhance: enhance = image.load(enhance).convert_alpha()
        if splash: splash = image.load(splash).convert_alpha()

        tmp_surface = Surface(base.get_size(), SRCALPHA)
        tmp_surface.fill((0, 0, 0, 0))
        tmp_hover_surface = tmp_surface.copy()
        self.surface = Surface(base.get_size(), SRCALPHA)
        self.hover_surface = Surface(base.get_size(), SRCALPHA)
        self.surface.fill((0, 0, 0, 0))
        self.hover_surface.fill((0, 0, 0, 0))

        if base:
            tmp_surface.blit(base, (0, 0))
            tmp_hover_surface.blit(hover, (0, 0))
        if mask:
            tmp_surface.blit(mask, (0, 0))
            tmp_hover_surface.blit(mask, (0, 0))
        if overlay:
            tmp_surface.blit(overlay, (0, 0), special_flags=BLEND_RGBA_MULT)
            tmp_hover_surface.blit(overlay, (0, 0), special_flags=BLEND_RGBA_MULT)
            tmp_hover_surface.blit(hover, (0, 0))
        if enhance:
            tmp_surface.blit(enhance, (0, 0))
            tmp_hover_surface.blit(enhance, (0, 0))
        if splash:
            self.surface.blit(splash, (0, 0))
            self.hover_surface.blit(splash, (0, 0))

        self.surface.blit(tmp_surface, (0, 0))
        self.hover_surface.blit(tmp_hover_surface, (0, 0))

        self.surface = scale(self.surface,
                    (self.surface.get_width()*SCALE,
                     self.surface.get_height()*SCALE))

        self.hover_surface = scale(self.hover_surface,
                    (self.hover_surface.get_width()*SCALE,
                     self.hover_surface.get_height()*SCALE))


if __name__ == "__main__":
    m = Monster(100, Monster.BOSS)