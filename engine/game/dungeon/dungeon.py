import logging
from random import randint, sample
from functools import reduce

import engine.game.monster.monster as monster
import engine.game.item.item as item
import engine.game.player.player as player
import engine.game.dungeon.location as location

class Dungeon(object):
  """Dungeon object holds all the possible routes as well as in charge of moving"""

  def __init__(self, level_type, difficulty, **kwargs):
    self.level = level_type
    #self.power = power
    self.difficulty = difficulty
    self.depth = 7
    self.min_width = 2
    self.max_width = 5
    self.min_branch = 1
    self.max_branch = 3 # not guaranteed
    self.min_shops = 1
    self.max_shops = 3
    self.min_alters = 0
    self.max_alters = 2
    self.min_monster = 5
    self.max_monster = 7
    self.min_items = 0
    self.max_items = 4
    # can be normal, low, high or bell
    self.branch_distribution = "normal"
    self.shop_distribution = "normal"
    self.alter_distribution = "normal"
    self.item_distribution = "normal"
    self.mon_distribution = "normal"

    for key in kwargs.keys():
      if key in ('min_width', 'max_width', 'min_branch', 'max_branch', 'min_shops', 'max_shops',
                 'min_alters', 'max_alters', 'min_item', 'max_item', 'min_monster', 'max_monster',
                 'branch_distribution', 'shop_distribution', 'alter_distribution', 'item_distribution',
                 'mon_distribution'):
        setattr(self, key, kwargs[key])

    self.start = location.Location("entrance", self.level)
    self.stop = location.Location("exit", self.level)

    # create the inbetween nodes
    frame = {}
    for i in range(self.depth):
      frame[i] = [location.Location("event", self.level) for i in range(randint(self.min_width, self.max_width))]

    for loc in frame[0]:
      self.start.set_neighbour(loc) # attach start to nodes

    # create distributions
    if self.branch_distribution == "normal":
      bdist = lambda x, y: randint(x, y)
    elif self.branch_distribution == "low":
      bdist = lambda x, y: min(randint(x, y), randint(x, y))
    elif self.branch_distribution == "high":
      bdist = lambda x, y: max(randint(x, y), randint(x, y))
    elif self.branch_distribution == "bell":
      bdist = lambda x, y: sorted([randint(x, y), randint(x, y), randint(x, y)])[1]

    for i in range(self.depth-1): # attach nodes to the end minus the last nodes
      used = set()
      for loc in frame[i]:
        branch = bdist(self.min_branch, self.max_branch)
        if branch > len(frame[i+1]): # overflow
          branch = len(frame[i+1])
        for neighbour in sample(frame[i+1], branch):
          loc.set_neighbour(neighbour)
          used.add(neighbour)

      for loc in frame[i+1]: # make sure that no nodes are left out might update
        if loc not in used: # adds the unused location to the lowest branched prev loc
          sorted(frame[i], key=lambda loc: len(loc.get_neighbours()))[0].set_neighbour(loc)

    for loc in frame[self.depth-1]:
      loc.set_neighbour(self.stop) # attach last nodes to exit

    # populate Dungeon
    nodes = reduce(lambda x, y: x + y, frame.values())

    # populate monsters
    # get monsters distributions
    if self.mon_distribution == "normal":
      mdist = lambda x, y: randint(x, y)
    elif self.mon_distribution == "low":
      mdist = lambda x, y: min(randint(x, y), randint(x, y))
    elif self.mon_distribution == "high":
      mdist = lambda x, y: max(randint(x, y), randint(x, y))
    elif self.mon_distribution == "bell":
      mdist = lambda x, y: sorted([randint(x, y), randint(x, y), randint(x, y)])[1]

    monster = mdist(self.min_monster, self.max_monster)
    if monster > len(nodes):
        # check for overflow means that if there is no space certain
        # nodes cannot be added
      logging.warning("All nodes are full only creating %d monster from %d monster"%(len(nodes), monster))
      monster = len(nodes)
    for node in sample(nodes, monster):
      node.set_type("monster")
      nodes.remove(node)

    # # populate shops
    # # get shop distributions
    # if self.shop_distribution == "normal":
    #   sdist = lambda x, y: randint(x, y)
    # elif self.shop_distribution == "low":
    #   sdist = lambda x, y: min(randint(x, y), randint(x, y))
    # elif self.shop_distribution == "high":
    #   sdist = lambda x, y: max(randint(x, y), randint(x, y))
    # elif self.shop_distribution == "bell":
    #   sdist = lambda x, y: sorted([randint(x, y), randint(x, y), randint(x, y)])[1]

    # shops = sdist(self.min_shops, self.max_shops)
    # if shops > len(nodes): # check for overflow means that if there is no space certain
    #                                     # nodes cannot be added
    #   logging.warning("All nodes are full only creating %d shops from %d shops"%(len(nodes), shops))
    #   shops = len(nodes)
    # for node in sample(nodes, shops):
    #   node.set_type("shop")
    #   nodes.remove(node)

    # # populate alters
    # # get shop distributions
    # if self.alter_distribution == "normal":
    #   adist = lambda x, y: randint(x, y)
    # elif self.alter_distribution == "low":
    #   adist = lambda x, y: min(randint(x, y), randint(x, y))
    # elif self.alter_distribution == "high":
    #   adist = lambda x, y: max(randint(x, y), randint(x, y))
    # elif self.alter_distribution == "bell":
    #   adist = lambda x, y: sorted([randint(x, y), randint(x, y), randint(x, y)])[1]

    # alters = adist(self.min_alters, self.max_alters)
    # if alters > len(nodes): # check for overflow means that if there is no space certain
    #                                     # nodes cannot be added
    #   logging.warning("All nodes are full only creating %d alters from %d alters"%(len(nodes), alters))
    #   alters = len(nodes)
    # for node in sample(nodes, alters):
    #   node.set_type("alter")
    #   nodes.remove(node)

    # # populate items
    # # get shop distributions
    # if self.item_distribution == "normal":
    #   idist = lambda x, y: randint(x, y)
    # elif self.item_distribution == "low":
    #   idist = lambda x, y: min(randint(x, y), randint(x, y))
    # elif self.item_distribution == "high":
    #   idist = lambda x, y: max(randint(x, y), randint(x, y))
    # elif self.item_distribution == "bell":
    #   idist = lambda x, y: sorted([randint(x, y), randint(x, y), randint(x, y)])[1]

    # items = idist(self.min_items, self.max_items)
    # if items > len(nodes): # check for overflow means that if there is no space certain
    #                                     # nodes cannot be added
    #   logging.warning("All nodes are full only creating %d items from %d items"%(len(nodes), items))
    #   items = len(nodes)
    # for node in sample(nodes, items):
    #   node.set_type("item")
    #   nodes.remove(node)
    # for loc in frame.values():
    #   #print(loc)
    #   pass

    self.frame = [[self.start]]+[value for value in frame.values()]+ \
        [[self.stop]]

    #print(*["Depth %d: [%s]"%(i, ", ".join(loc.loc_type for loc in locs)) for i, locs in frame.items()], sep="\n")


# Test
if __name__ == "__main__":

  d = Dungeon("prison", "normal", depth=5)

  def add_name(loc):
    v = set()
    n = [loc]
    counter = 0
    while n:
      cur = n.pop(0)
      cur.name = counter
      counter += 1
      for loc in cur.get_neighbours():
        if loc not in v:
          n.append(loc)
          v.add(loc)

  def recurse(loc):
    v = set()
    n = [loc]
    while n:
      cur = n.pop(0)
      print(cur.name, ":= ", *[n.name for n in cur.get_neighbours()])
      for loc in cur.get_neighbours():
        if loc not in v:
          n.append(loc)
          v.add(loc)
  add_name(d.start)
  recurse(d.start)
