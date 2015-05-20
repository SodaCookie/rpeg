from itertools import chain
from random import choice
import dialog

class Location(object):
  """Location object is the node for each part of a dungeon"""
  def __init__(self, loc_type, level):
    self.loc_type = loc_type # can be event, entrance, exit, shop, alter, item
    self.level = level
    self.locked = False # to be implemented
    self.blocked = False # to be implemented
    self.dialog_cache = None
    self.neighbours = []

  def open(self):
    """Returns the dialog found at this location"""
    if not self.dialog_cache:
      self.dialog_cache = dialog.Dialog("main", self.event)
    return self.dialog_cache

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

  def traverse(self, index):
    return self.neighbours[index]

  def generate(self, etree):
    """Method is used to generate event based off the situation of the node"""
    possible_dialogs = list(chain(etree.findall("event[@type='%s'][@level='%s']"%(self.loc_type, self.level)),\
                                            etree.findall("event[@type='%s'][@level='%s']"%(loc_type, "any"))))
    self.event = choice(possible_dialogs)
    # this method will use the number of incoming nodes, out going nodes, adjacent tags and tags to determine the description

if __name__ == "__main__":
  import xml.etree.ElementTree as tree
  #from lxml import etree as tree #optional version of the tree in case we need faster parsing
  with open("data/test_data.xml", "r") as file:
    etree = tree.parse(file)
  loc = Location("event", "test", etree)