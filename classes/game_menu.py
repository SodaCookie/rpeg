import random

import classes.rendering.view as view
from classes.party_menu import PartyMenu
from classes.event_menu import EventMenu
from classes.travel_menu import TravelMenu
from classes.battle_info_menu import BattleInfoMenu
from classes.loot_menu import LootMenu
from classes.monster_menu import MonsterMenu
from classes.sidebar import SideBar
from classes.bars import Bars
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
        self.battle = None
        self.current_target = None
        self.current_char = None
        self.updated_icons = False

        self.background = Image((0,0), filename="images/ui/background.png", h_anchor=1, v_anchor=1)
        self.background.display()
        self.party_menu = PartyMenu(self.party, self.set_character)
        self.event_menu = EventMenu(self.current_location, self.party, self)
        self.travel_menu = TravelMenu(self.current_location, self.travel)
        self.battle_info_menu = None
        self.bars = Bars()
        self.bars.add(self.party_menu.bars)
        self.shop_menu = None
        self.loot_menu = None
        self.alter_menu = None
        self.monster_menu = None
        self.sidebar = SideBar(self)
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
        self.sidebar.loot.display()

    def create_monster(self):
        monsters = [monster.Monster(100, random.randint(0,2)) for i in range(3)]
        self.battle = battle.Battle(self.party.players, monsters)
        self.monster_menu = MonsterMenu(monsters)
        self.sidebar.hide()
        self.bars.add(self.monster_menu.bars)

    def create_shop(self):
        pass

    def set_character(self, character):
        self.current_char = character
        is_battle = bool(self.battle)
        is_limited = False
        if self.battle_info_menu:
            self.bars.remove(self.battle_info_menu.bars)
            self.battle_info_menu.delete()
        self.battle_info_menu = BattleInfoMenu(character,
            is_battle, is_limited)
        self.bars.add(self.battle_info_menu.bars)
        self.battle_info_menu.display()

    def travel(self, location):
        """Returns given location"""
        self.current_location = location

    def handle_battle(self, delta):
        self.bars.update()

        if self.current_char:
            if self.current_char.ready and not self.updated_icons:
                self.battle_info_menu.icons.update(self.current_char.ready)
                self.updated_icons = True
            elif not self.current_char.ready and self.updated_icons:
                self.battle_info_menu.icons.update(self.current_char.ready)
                self.updated_icons = False

        for monster in self.battle.monsters:
            if monster.ready:
                monster.cast("hello", self.battle)

    def set_current_character(self, character):
        self.current_char = character
        self.render_battle_info()