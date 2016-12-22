from engine.game.attribute.attribute import Attribute

class Stitched(Attribute):

    def __init__(self, amount):
        """Attribute decreases defense by amount as the character gets hit.""
        amount -> float"""
        super().__init__("stitched-%s"%amount)
        self.amount = float(amount)
        self.reduction_factor = 0

    def on_damage(self, source, damage, damage_type):
        self.reduction_factor += self.amount

    def on_get_stat(self, value, stat_type):
        if stat_type == "defense":
            return value - self.reduction_factor
        return value

    def description(self):
        return "Lowers defense by %d." % self.reduction_factor
