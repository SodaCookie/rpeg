from engine.game.move.component import Component

class Message(Component):
    """Component that will return a message"""
    def __init__(self, message):
        self.message = message

    def on_cast(self, target, caster, players, monsters):
        print(self.message)
        return self.message