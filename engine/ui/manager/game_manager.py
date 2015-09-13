from engine.ui.core.manager import Manager
import engine.ui.manager as manager

class GameManager(Manager):
    """GameManager is responsible for rendering and updating
    all the various gameplay related elements in the game
    it also controls pseudorandom ordering of menu systems
    in the form of the manager list. It is also in charge of macro
    level logic of the rendering of the menus."""

    def __init__(self):
        super(GameManager, self).__init__()
        self.managers = [
            manager.EventManager()
            manager.PartyManager(),
            manager.EncounterManager(),
            manager.CastBarManager(),
        ]