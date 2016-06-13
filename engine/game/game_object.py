"""Define GameObject"""
from engine.game.party.party import Party

class GameObject(object):
    """Game object used to hold all the data required for
    rendering and holding the important info for the game"""

    DUNGEON_TYPES = ["catacomb"]

    def __init__(self):
        super().__init__()
        self.difficulty = "normal"
        self.floor_level = 1
        self.floor_type = ""
        self.current_location = None
        self.current_dialogue = None

        self.party = Party()
        self.encounter = []
        self.current_dialogue = None

        self.shop = None
        self.alter = None
        self.loot = None

        self.mouse_button = (0, 0, 0)
        self.mouse_x = 0
        self.mouse_y = 0
        self.resolution = (0, 0)

        self.current_player = None
        self.hover_data = None

        self.render_travel = False
