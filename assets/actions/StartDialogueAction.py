from engine.game.dungeon.action import Action

class StartDialogueAction(Action):

    def __init__(self, dialogue):
        """Begin a new dialogue in the event.
        dialogue -> str"""
        super().__init__()
        self.dialogue = dialogue

    def execute(self, game):
        """Starts a new dialogue tree."""
        game.current_dialogue = self.dialogue