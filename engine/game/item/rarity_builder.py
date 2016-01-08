from engine.game.item.builder import Builder

class RarityBuilder(Builder):

    NAME = "rarity"

    def __init__(self, rarity):
        super().__init__(2, rarity)

    def build_rarity(self, distribution):
        if self.value == "common":
            distribution["common"] = 100
            distribution["rare"] = -1
            distribution["epic"] = -1
            distribution["legendary"] = -1
        elif self.value == "rare":
            distribution["common"] = -1
            distribution["rare"] = 100
            distribution["epic"] = -1
            distribution["legendary"] = -1
        elif self.value == "epic":
            distribution["common"] = -1
            distribution["rare"] = -1
            distribution["epic"] = 100
            distribution["legendary"] = -1
        elif self.value == "legendary":
            distribution["common"] = -1
            distribution["rare"] = -1
            distribution["epic"] = -1
            distribution["legendary"] = 100

        return distribution

    def build_stats(self, stats, tag, rarity, type):
        """Override if the builder defines how to build stats"""
        if rarity == "common":
            stats["points"] = stats["points"] * 1
        elif rarity == "rare":
            stats["points"] = stats["points"] * 1.2
        elif rarity == "epic":
            stats["points"] = stats["points"] * 1.5
        elif rarity == "legendary":
            stats["points"] = stats["points"] * 2
        return stats