from engine.game.attribute.attribute import Attribute

class LowerStat(Attribute):

    def __init__(self, amount, stype):
        """Attribute that lowers a stat of a player
        amount -> float
        stype -> str"""
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