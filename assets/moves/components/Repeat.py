from engine.game.move.component import Component

class Repeat(Component):
    """Component that will complete another component x times"""
    def __init__(self, repeat, component):
        self.repeat = repeat
        self.component = component

    def on_cast(self, target, caster, players, monsters):
        msg = ""
        for i in range(self.repeat):
            msg += self.component.on_cast(target, caster, players, monsters)+'\n'
        return msg