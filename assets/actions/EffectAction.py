from engine.game.dungeon.action import Action
from engine.system import Message

class EffectAction(Action):

    def __init__(self, effect):
        """Begin a new dialogue in the event.
        effect -> Effect"""
        super().__init__()
        self.effect = effect

    def execute(self, game, system):
        """Changes party shards by given amount tree."""
        system.message("game", Message("apply-effect", self.effect))