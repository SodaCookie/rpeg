from engine.game.dungeon.action import Action
from engine.system import Message

class StartDialogueAction(Action):

    def __init__(self, dialogue):
        """Begin a new dialogue in the event.
        dialogue -> str"""
        super().__init__()
        self.dialogue = dialogue

    def execute(self, game, system):
        """Starts a new dialogue tree."""
        system.message("game", Message("dialogue", self.dialogue))