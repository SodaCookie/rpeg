from engine.game.dungeon.action import Action

class StartDialogueAction(Action):

    def __init__(self, dialogue):
        super().__init__()
        self.dialogue = dialogue

    def execute(self, game):
        """Starts a new dialogue tree."""
        game.current_dialog = self.dialogue