from engine.game.attribute.attribute import Attribute

class RaiseStat(Attribute):

    def __init__(self, amount, stype):
        """Attribute that raises a stat of a player.
        amount -> float
        stype -> str"""
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