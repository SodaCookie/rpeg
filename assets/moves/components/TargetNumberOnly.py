from engine.game.move.component import Component

class TargetNumberOnly(Component):
    """Descriptor for targetting a specific number of characters only"""
    def __init__(self, number):
        self.number = number

    def valid_cast(self, selected, caster, players, monsters):
        return len(selected) == self.number

    def valid_target(self, selected, caster, players, monsters):
        return len(selected) <= self.number
