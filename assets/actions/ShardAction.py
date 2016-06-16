from engine.game.dungeon.action import Action
from engine.system import Message

class ShardAction(Action):

    def __init__(self, shards):
        """Begin a new dialogue in the event.
        shards -> int"""
        super().__init__()
        self.shards = shards

    def execute(self, game, system):
        """Changes party shards by given amount tree."""
        system.message("game", Message("shard", self.shards))