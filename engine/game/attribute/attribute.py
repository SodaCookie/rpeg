import enginge.game.effect.effect as effects

class Attribute(effect.Effect):
  """Attributes are permanent effects that are applied through items
  they are also stackable (additively) unlike buffs. Attributes will
  only be applied once per beginning of a battle"""

  def __init__(self, name):
    super().__init__(name, effect.Effect.PERMANENT)

  def __str__(self):
      return "%s<attribute> - %s" % (self.name.replace("-", " ").title(),
                                 self.duration)

  def description(self):
    """Returns a string describing the attributes function"""
    return ""

