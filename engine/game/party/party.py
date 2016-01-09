class Party(object):
  """Object to hold and access information about the party.
  Party is composed of the players, gold and items in the party."""

  def __init__(self, players):
    self.players = players
    self.gold = 0
    self.items = [] # strings, items that the party owns like "orb"

  def has_gold(self, amount):
    """Returns True if party has enough gold"""
    return amount >= self.gold

  def add_gold(self, amount):
    self.gold += amount

  def remove_gold(self, amount):
    self.gold -= amount

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