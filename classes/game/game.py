import classes.rendering.view as view

class Game(object):
    """Game object used to hold all the data required for
    rendering and holding the important info for the game"""

    DUNGEON_TYPES = ["catacomb", "caverns"]
    POWER_PER_LEVEL = 100

    def __init__(self, party):
        super(Game, self).__init__()
        self.difficulty = "normal"
        self.power = Game.POWER_PER_LEVEL
        self.level_type = ""
        self.party = party
        self.current_location = None
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
        self.cast_type = ""