"""A compilation of the attributes built for the game"""

from engine.game.attribute.attribute import Attribute

class RaiseStat(Attribute):
  """Attribute that raises a stat of a player"""

  def __init__(self, amount, stype):
    super().__init__("raise-%s"%stype)
    self.amount = float(amount)
    self.stype = stype

  def on_refresh(self, buff):
    self.amount += buff.amount

  def on_get_stat(self, value, stat_type):
    if self.stype == stat_type:
      return value * (1+self.amount)
    return value

  def description(self):
    return "Gain +%d%% bonus %s stat" % (int(100*self.amount), self.stype)


class LowerStat(Attribute):
  """Attribute that lowers a stat of a player"""

  def __init__(self, amount, stype):
    super().__init__("lower-%s"%stype)
    self.amount = float(amount)
    self.stype = stype

  def on_refresh(self, buff):
    self.amount += buff.amount

  def on_get_stat(self, value, stat_type):
    if self.stype == stat_type:
      return value * (1-min(1, self.amount))
    return value

  def description(self):
    return "Decrease +%d%% %s stat" % (int(1-min(1, self.amount)), self.stype)