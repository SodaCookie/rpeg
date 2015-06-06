import classes.rendering.view as view
from classes.party_menu import PartyMenu
from classes.event_menu import EventMenu
from classes.travel_menu import TravelMenu
from classes.loot_menu import LootMenu
from classes.sidebar import SideBar
from classes.image_cache import ImageCache
from classes.rendering.dragable import Dragable
from classes.rendering.image import Image
from classes.rendering.text import Text, TextInfo
from classes.rendering.button import Button, ButtonInfo
from classes.controller import BattleController

import classes.game.dungeon as dungeon
import classes.game.party as party
import classes.game.player as player
import classes.game.monster as monster
import classes.game.shop as shop
import classes.game.battle as battle


class GameMenu(BattleController):

    POWER_PER_LEVEL = 100

    def __init__(self):
        super().__init__()

        players = [player.Player("Test Player") for i in range(4)]
        self.level = 1
        self.power = self.level*GameMenu.POWER_PER_LEVEL
        self.dungeon = dungeon.Dungeon(self.level)
        self.party = party.Party(players)
        self.resolution = view.get_resolution()
        self.current_location = self.dungeon.start
        self.current_location.generate()
        self.current_dialog = None
        self.current_battle = None
        self.current_target = None
        self.current_char = players[0]

        self.text_style = TextInfo(fontcolor=(255,255,255),
                                   fontsize=16,
                                   alignment=-1,
                                   h_anchor=1,
                                   v_anchor=1,
                                   wrap=True,
                                   width=149*view.SCALE)

        self.button_title_style = TextInfo(fontcolor=(255,255,255),
                                   fontsize=30,
                                   alignment=-1,
                                   h_anchor=0,
                                   v_anchor=0)

        self.loot_style = TextInfo(fontcolor=(255,255,255),
                                   fontsize=30,
                                   alignment=0,
                                   h_anchor=0,
                                   v_anchor=-1,
                                   wrap=True,
                                   width=149*view.SCALE);

        # self.large_button_style = ButtonInfo(self.button_style, h_anchor=0, v_anchor=0);

        self.background = Image((0,0), filename="images/ui/background.png", h_anchor=1, v_anchor=1)
        self.background.display()
        self.party_menu = PartyMenu(self.party)
        self.event_menu = EventMenu(self.current_location, self.party, self)
        self.travel_menu = TravelMenu(self.current_location, self.travel)
        self.shop_menu = None
        self.loot_menu = None
        self.alter_menu = None
        self.monster_menu = None
        self.sidebar = SideBar(self.display_travel, self.display_shop)
        self.party_menu.display()
        self.event_menu.display()
        self.sidebar.travel.display()

    def display_travel(self):
        self.travel_menu.display()

    def display_shop(self):
        self.shop_menu.display()

    def display_loot(self):
        self.loot_menu.display()

    def display_alter(self):
        self.alter_menu.display()

    def display_monster(self):
        self.monster_menu.display()

    def create_alter(self):
        pass

    def create_loot(self, gold, items):
        self.loot_menu = LootMenu(self.party, gold, items)

    def create_monster(self):
        pass

    def create_shop(self):
        pass

    def travel(self, location):
        """Returns given location"""
        self.current_location = location

    def handle_battle(self, delta):
        for monster in self.current_battle.monsters:
            if monster.ready:
                monster.cast("hello", self.current_battle)

    def set_current_character(self, character):
        self.current_char = character
        self.render_battle_info()