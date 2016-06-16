from engine.game.move.component import Component

class Conditional(Component):
    """Component that will execute list of components 1 if given predicate is
    True else will execute list of components 2"""

    def __init__(self, predicate, components1, components2):
        """Executes a list of components depending on the outcome of the the predicate.
        predicate -> lambda (target, caster, players, monsters)
        components1 -> list Component
        components2 -> list Component"""
        self.predicate = predicate
        self.components1 = components1
        self.components2 = components2

    def on_cast(self, target, caster, players, monsters, system):
        msg = ""
        if self.predicate(target, caster, players, monsters):
            for component in self.components1:
                msg += component.on_cast(target, caster, players, monsters,
                    system)
            return msg
        else:
            for component in self.components2:
                msg += component.on_cast(target, caster, players, monsters,
                    system)
            return msg