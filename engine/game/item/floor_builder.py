import random
from engine.game.item.builder import Builder

class FloorBuilder(Builder):

    NAME = "floor"

    def __init__(self, value):
        if value == None: # bad code
            value = 1
        super().__init__(1, value)

    def build_stats(self, stats, tag, rarity, type):
        stats["points"] = round(self.value*6*(1+(random.random()*0.2-0.1)))
        return stats # 5 is growth constant per floor, 0.2 and 0.1 are distribution +/- of stat