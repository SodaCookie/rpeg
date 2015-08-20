import classes.rendering.view as view
from classes.game.party import Party

class Game(object):
    """Game object used to hold all the data required for
    rendering and holding the important info for the game"""

    DUNGEON_TYPES = ["catacomb", "caverns"]
    POWER_PER_LEVEL = 100

    def __init__(self, party):
        super(Game, self).__init__()
        self.difficulty = "normal"
        self.power = Game.POWER_PER_LEVEL
        self.level = 1 # the floor level
        self.level_type = "" # the type of floor
        self.party = Party(party)
        self.current_event = None
        self.current_location = None
        self.current_move = None
        self.current_character = None # used for user info
        self.current_selection = None # used for battle
        self.monsters = []
        self.dungeon = None
        self.shop = None
        self.alter = None
        self.loot = None
        self.battle = None
        self.is_battle = None
        self.resolution = view.get_resolution()
        self.hover_character = None
