from random import randint, choice
import xml.etree.ElementTree as tree
import objects.attribute as attribute
import re

class Item:

  POWER_BASE = 1.1 # how many more stat points a rarity gives
  ATTACK_HEURISTIC = 1
  DEFENSE_HEURISTIC = 1
  RESIST_HEURISTIC = 1
  HEALTH_HEURISTIC = 0.2
  SPEED_HEURISTIC = 3
  MAGIC_HEURISTIC = 1
  INPUT_PATTERN = re.compile("\[(.*?)\]", re.IGNORECASE)
  _XML = tree.parse("data/item.xml")
  TAGS = _XML.findall("tags/tag") # all tags including bad tags
  NAMES = _XML.find("names")
  ATTRIB = _XML.find("attributes")
  TYPES = _XML.find("types")

  def __init__(self, power, rarity, generate=True):
    """Generate indicates whether or not you want to auto generate an item"""
    self.name = "None"
    self.power = power
    self.rarity = rarity
    self.type = "" # item type (sword, shield, etc..)
    self.slot = "" # where the item is equipped
    self.attack = 0
    self.defense = 0
    self.health = 0
    self.magic = 0
    self.resist = 0
    self.speed = 0
    self.attributes = []

    if generate: self.generate()

  def generate(self):

    # generate tags based on rarity
    if self.rarity == "legendary":
      num_tags = 4
    elif self.rarity == "epic":
      num_tags = 3
    elif self.rarity == "rare":
      num_tags = 2
    else:
      num_tags = 1

    # generate a bad tag (negative attribute)
    bad_tag = 0
    if randint(0, 9) < 1: # 10% chance of a negative roll one add a
                 # negative roll
      if randint(0, 1): # after there is a 50/50 chance of more stats or
                # another tag
        num_tags += 1
      else:
        self.power = self.power*Item.POWER_BASE
      bad_tag = 1

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

    # roll for attributes
    attribute_rolls = []
    for tag in tags:
      attribute_rolls.append(choice(Item.ATTRIB.findall(
                             "attribute[@type='%s'][@rarity='%s']"
                             %(tag.attrib["type"], self.rarity))))

    # roll bad attribute
    if bad_tag:
      attribute_rolls.append(choice(Item.ATTRIB.findall(
                             "attribute[@type='bad']")))
    #print(list(t.attrib["type"] for t in tags)) # testing
    for attrib in attribute_rolls:
      args = attrib.text.split(' ') # name, arg1, arg2, arg3...
      self.attributes.append(attribute.attributes[args[0]](*args[1:]))

    # generate type
    item_type = choice(Item.TYPES.findall("type"))
    self.slot = item_type.attrib["slot"]
    self.type = item_type.attrib["name"]

    # affect weights with type
    attack_weight = 1 # higher attack stats
    defense_weight = 1 # higher defense stats
    resist_weight = 1 # higher resist stats
    speed_weight = 1 # higher speed stats
    health_weight = 1 # higher health stats
    magic_weight = 1 # higher magic stats

    if item_type.attrib.get("attack"):
      attack_weight += float(item_type.attrib["attack"])
    if item_type.attrib.get("defense"):
      defense_weight += float(item_type.attrib["defense"])
    if item_type.attrib.get("resist"):
      resist_weight += float(item_type.attrib["resist"])
    if item_type.attrib.get("speed"):
      speed_weight += float(item_type.attrib["speed"])
    if item_type.attrib.get("health"):
      health_weight += float(item_type.attrib["health"])
    if item_type.attrib.get("magic"):
      magic_weight += float(item_type.attrib["magic"])

    # generate stats
    for tag in tags:
      if tag.attrib.get("attack"):
        attack_weight += float(tag.attrib["attack"])
      if tag.attrib.get("defense"):
        defense_weight += float(tag.attrib["defense"])
      if tag.attrib.get("resist"):
        resist_weight += float(tag.attrib["resist"])
      if tag.attrib.get("speed"):
        speed_weight += float(tag.attrib["speed"])
      if tag.attrib.get("health"):
        health_weight += float(tag.attrib["health"])
      if tag.attrib.get("magic"):
        magic_weight += float(tag.attrib["magic"])

    r1, r2, r3, r4, r5, r6 = [randint(0,100) for i in range(6)]
    r1 = r1 * attack_weight
    r2 = r2 * defense_weight
    r3 = r3 * speed_weight
    r4 = r4 * health_weight
    r5 = r5 * magic_weight
    r6 = r6 * resist_weight
    s = r1 + r2 + r3 + r4 + r5 + r6 # Divide the power into 6 random parts

    self.attack = round(self.power*r1/s/Item.ATTACK_HEURISTIC)
    self.defense = round(self.power*r2/s/Item.DEFENSE_HEURISTIC)
    self.health = round(self.power*r3/s/Item.HEALTH_HEURISTIC)
    self.speed = round(self.power*r4/s/Item.SPEED_HEURISTIC)
    self.magic = round(self.power*r5/s/Item.MAGIC_HEURISTIC)
    self.resist = round(self.power*r6/s/Item.RESIST_HEURISTIC)

    # generate name
    if self.rarity == "legendary":
      if bad_tag:
        template = "[adverb] [adjective] [item] of [bad] [noun]"
      else:
        template = "[adverb] [adjective] [item] of [adjective] [noun]"
    elif self.rarity == "epic":
      if bad_tag:
        template = "[bad] [item] of [adjective] [noun]"
      else:
        template = "[adjective] [item] of [adjective] [noun]"
    elif self.rarity == "rare":
      if bad_tag:
        template = "[bad] [item] of [noun]"
      else:
        template = "[adjective] [item] of [noun]"
    else:
      if bad_tag:
        template = "[bad] [item]"
      else:
        template = "[adjective] [item]"

    counter = 0
    for match in Item.INPUT_PATTERN.finditer(template):
      if match.group(1) == "bad": # gotta find bad keyword
        replacements = Item.NAMES.findall("name[@type='bad'][@rarity='%s']"
                                          % self.rarity)
      elif match.group(1) == "item":
        template = template.replace(match.group(0), self.type)
        continue
      else:
        replacements = Item.NAMES.findall(
                         "name[@type='%s'][@rarity='%s'][@speech='%s']"
                          % (tags[counter].attrib["type"],
                          self.rarity, match.group(1)))
        counter += 1
      template = template.replace(match.group(0), choice(replacements).attrib["word"])
    self.name = template.title()


if __name__ == "__main__":
  import os
  os.chdir("..")
  ITERATIONS = 10
  li = []
  for i in range(ITERATIONS):
    li.append(Item(100, "common"))
    print(li[-1].name, li[-1].attributes)