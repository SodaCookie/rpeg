from random import choice, randint
import xml.etree.ElementTree as tree

from pygame import image, Surface

import objects.character as character

class Monster(character.Character):

    _XML = tree.parse("data/item.xml")
    TAGS = _XML.findall("tags/tag") # all tags including bad tags
    NAMES = _XML.find("names")
    IMAGE = _XML.find("images")
    TYPES = _XML.find("mtypes")

    def __init__(self, power, difficulty = "common", mtype=""):
        """Power is used to calculate the amount of stats the monster is
        given. difficulty will modify a few things about the monster
        for example 1 is a normal spawn but 2 is a elite mob and a
        3 is a boss mob"""
        super().__init__("")
        self.difficulty = difficulty
        self.monster = monster
        self.tags = []
        self.mtype = mtype
        self.attack = 0
        self.defense = 0
        self.resist = 0
        self.magic = 0
        self.current_health = 100
        self.health = 100
        self.speed = 0
        self.power = power
        self.name = "Jeremy's Face"
        self.surface = image.load("images/monster/test_monster.png").convert_alpha()
        self.generate_tags()
        self.generate_name()
        self.generate_stats(power)

    def generate_tags(self):
        # generate tags
        if self.difficulty == "common":
          num_tags = randint(1, 2)
        elif self.difficulty == "elite":
          num_tags = randint(2, 3)
        elif self.difficulty == "boss":
          num_tags = max(randint(2, 3), randint(2, 3))

        # roll for tags
        tags = [choice(Item.TAGS) for i in range(num_tags)]
        # fix exclusions (first come first serve) will be replaced with a tag
        # before it. Based off the first tag
        excludes = set(tags[0].attrib.get("exclude").split(', ')) or not set()
        for i, tag in enumerate(tags):
          if tag.attrib["type"] in excludes:
            tags[i] = tags[i-1]
          else: # add more exclusions if any
            excludes.union(set(tag.attrib.get("exclude").split(', ') or not set()))

    def generate_stats(self):
        """Generates stats based on the power level of the players"""
        pass

    def generate_name(self):
        pass
