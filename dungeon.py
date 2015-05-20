import monster
import item
import player
import location

class Dungeon(object):
  """Dungeon object holds all the possible routes as well as in charge of moving"""

  def __init__(self, level, **kwargs):
    self.depth = 10
    self.min_width = 2
    self.max_width = 5
    self.min_branch = 1
    self.max_branch = 3
    self.min_shops = 1
    self.max_shops = 3
    self.min_alters = 0
    self.max_alters = 2
    self.min_item = 0
    self.max_item = 4

    for key in kwargs.keys():
      if self.depth = 10
      elif key == "min_width": min_width = kwargs[key]
      elif key == "max_width": max_width = kwargs[key]
      elif key == "min_branch": min_branch = kwargs[key]
      elif key == "max_branch": max_branch = kwargs[key]
      elif key == "min_shops": min_shops = kwargs[key]
      elif key == "max_shopes": max_shops = kwargs[key]
      elif key == "min_alters": min_alters = kwargs[key]
      elif key == "max_alters": max_alters = kwargs[key]
      elif key == "min_item": min_item = kwargs[key]
      elif key == "max_item": max_item = kwargs[key]

    for i in range(self.depth):
      pass