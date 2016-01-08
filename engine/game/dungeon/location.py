from itertools import chain
from random import choice
import xml.etree.ElementTree as tree
import re

import engine.game.dungeon.dialog as dialog

class Location(object):
  """Location object is the node for each part of a dungeon"""

  ROOM_TYPE = {
               "default" : ["room"]}
  INPUT_PATTERN = re.compile("\[(.*?)\]", re.IGNORECASE)
  EVENTS = tree.parse("data/scenario.xml")

  def __init__(self, loc_type, level):
    self.loc_type = loc_type # can be event, entrance, exit, shop, alter, item
    self.description = "" # description is presented to the user after generation
    self.tags = []
    self.level = level
    self.locked = False # to be implemented
    self.blocked = False # to be implemented
    self.dialog_cache = None
    self.neighbours = []

  def get_event(self):
    """Returns the event found at this location"""
    if not self.dialog_cache:
      self.dialog_cache = dialog.Dialog("main", self.event)
    return self.dialog_cache

  def get_event_name(self):
    return self.event.attrib["name"]

  def set_block(self):
    self.blocked = True

  def set_lock(self):
    self.locked = True

  def set_type(self, loc_type):
    self.loc_type = loc_type

  def set_neighbour(self, location):
    self.neighbours.append(location)

  def get_neighbours(self):
    return self.neighbours

  def generate(self):
    """Method is used to generate event and description based off the situation of the node"""
    etree = Location.EVENTS
    possible_dialogs = list(chain(etree.findall("event[@type='%s'][@level='%s']"%(self.loc_type, self.level)), etree.findall("event[@type='%s'][@level='%s']"%(self.loc_type, "any"))))
    self.event = choice(possible_dialogs)

    if self.loc_type == "entrance": # special descriptions of types for ends
      return

    if self.loc_type == "exit":
      return

    # this method will use the number of incoming nodes, out going nodes, adjacent tags and tags to determine the description
    if Location.ROOM_TYPE.get(len(self.get_neighbours())) != None:
      room_type = choice(Location.ROOM_TYPE[len(self.get_neighbours())])
    else:
      room_type = choice(Location.ROOM_TYPE["default"])

    tag = self.event.find("tag")
    tags = {}
    if tag is not None:
      tags = dict((t.split('@') for t in tag.text.split(', ')))

    # find an appropriate template and fill the template
    with open("data/description.xml", "r") as file:
      desc = tree.parse(file)
    template = desc.findall("templates/template[@type='%s']"%room_type)
    text = choice(template).text # pick a template
    for match in Location.INPUT_PATTERN.finditer(text):
      # match group 0 is with brackets group 1 is without
      if tags.get(match.group(1)) != None:
        replacement = tags[match.group(1)]
      else:
        replacement = choice(desc.find(match.group(1)).text.split(', '))
      text = text.replace(match.group(0), replacement) # fill in the gaps
    self.description = text

  def __repr__(self):
    return self.loc_type


if __name__ == "__main__":
  #from lxml import etree as tree #optional version of the tree in case we need faster parsing
  with open("data/scenario.xml", "r") as file:
    etree = tree.parse(file)
  loc = Location("event", "test")
  loc.generate(etree)
  print(loc.description)