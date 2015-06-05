from random import choice, randint
import xml.etree.ElementTree as tree

from pygame import image, Surface, SRCALPHA, BLEND_RGBA_MULT

import objects.character as character

class Monster(character.Character):

    COMMON = 0
    ELITE  = 1
    BOSS = 2

    _XML = tree.parse("data/monster.xml")
    TAGS = _XML.findall("tags/tag") # all tags including bad tags
    NAMES = _XML.find("names")
    IMAGE = _XML.find("image")
    TYPES = _XML.findall("mtypes/mtype")

    def __init__(self, power, difficulty = 0, mtype="", name="Monster"):
        """Power is used to calculate the amount of stats the monster is
        given. difficulty will modify a few things about the monster
        for example 1 is a normal spawn but 2 is a elite mob and a
        3 is a boss mob"""
        super().__init__("")
        self.difficulty = difficulty
        self.tags = []
        self.mtype = mtype
        self.power = power
        self.name = name
        self.surface = None
        self.generate_tags()
        self.generate_name()
        self.generate_stats()
        self.generate_surface()

    def generate_tags(self):
        # generate tags
        if self.difficulty == Monster.COMMON:
          num_tags = randint(1, 2)
        elif self.difficulty == Monster.ELITE:
          num_tags = randint(2, 3)
        elif self.difficulty == Monster.BOSS:
          num_tags = max(randint(2, 3), randint(2, 3))

        # roll for tags
        tags = [choice(Monster.TAGS) for i in range(num_tags)]
        # fix exclusions (first come first serve) will be replaced with a tag
        # before it. Based off the first tag
        excludes = set(tags[0].attrib.get("exclude").split(', ')) or not set()
        for i, tag in enumerate(tags):
          if tag.attrib["type"] in excludes:
            tags[i] = tags[i-1]
          else: # add more exclusions if any
            excludes.union(set(tag.attrib.get("exclude").split(', ') or not set()))
        self.tags = tags

        # roll for monster type
        if not self.mtype:
            self.mtype = choice(Monster.TYPES).attrib["type"]

    def generate_stats(self):
        """Generates stats based on the power level of the players"""
        pass

    def generate_name(self):
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
        if overlay: overlay = image.load(overlay).convert_alpha()
        if enhance: enhance = image.load(enhance).convert_alpha()
        if splash: splash = image.load(splash).convert_alpha()

        tmp_surface = Surface(base.get_size(), SRCALPHA)
        tmp_surface.fill((0, 0, 0, 0))
        self.surface = Surface(base.get_size(), SRCALPHA)
        self.surface.fill((0, 0, 0, 0))

        if base:
            tmp_surface.blit(base, (0, 0))
        if mask:
            tmp_surface.blit(mask, (0, 0))
        if overlay:
            tmp_surface.blit(overlay, (0, 0), special_flags=BLEND_RGBA_MULT)
        if enhance:
            tmp_surface.blit(enhance, (0, 0))
        if splash:
            self.surface.blit(splash, (0, 0))
        self.surface.blit(tmp_surface, (0, 0))


if __name__ == "__main__":
    m = Monster(100, Monster.BOSS)