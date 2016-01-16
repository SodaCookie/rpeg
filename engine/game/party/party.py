class Party(object):
  """Object to hold and access information about the party.
  Party is composed of the players, shards and items in the party."""

  def __init__(self, players):
    self.players = players
    self.shards = 0

  def has_shards(self, amount):
    """Returns True if party has enough shards"""
    return amount >= self.shards

  def add_shards(self, amount):
    self.shards += amount

  def remove_shards(self, amount):
    self.shards -= amount
    if self.shards < 0:
      self.shards = 0

  def has_item(self, item):
    """Return True if party has item"""
    return item in self.items

  def add_item(self, item):
    self.items.append(item)

  def remove_item(self, item):
    """Removes item"""
    self.items.remove(item)

  def has_race(self, race):
    return race in [member.race for member in self.players]

  def has_item_type(self, wtype):
    for member in self.players:
      for item in member.equipment.values():
        if wtype == item.type:
          return True
    return False


if __name__ == "__main__":
  pass