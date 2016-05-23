from engine.game.move.component import Component

class TargetNumberOnly(Component):

    def __init__(self, number):
        """Descriptor for targeting a specific number of characters only.
        number -> int"""
        self.number = number

    def valid_cast(self, selected, caster, players, monsters):
        return len(selected) == self.number

    def valid_target(self, selected, caster, players, monsters):
        return len(selected) <= self.number
