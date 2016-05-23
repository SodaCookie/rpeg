from engine.game.move.component import Component

class Message(Component):
    def __init__(self, message):
        """Component that will return a message.
        message -> str"""
        self.message = message

    def on_cast(self, target, caster, players, monsters):
        print(self.message)
        return self.message