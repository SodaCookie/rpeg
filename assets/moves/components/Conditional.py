from engine.game.move.component import Component

class Conditional(Component):
    """Component that will execute list of components 1 if given condition is
    True else will execute list of components 2"""

    def __init__(self, condition, components1, components2):
        self.condition = condition
        self.components1 = components1
        self.components2 = components2

    def on_cast(self, target, caster, players, monsters):
        msg = ""
        if self.condition(target, caster, players, monsters):
            for component in self.components1:
                msg += component.on_cast(target, caster, players, monsters)
            return msg
        else:
            for component in self.components2:
                msg += component.on_cast(target, caster, players, monsters)
            return msg