import random

import pygame

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

from classes.game.game import Game
from classes.game.dungeon import Dungeon
from classes.game.party import Party
from classes.game.player import Player
from classes.game.monster import Monster
from classes.game.shop import Shop
from classes.game.battle import Battle
from classes.game.moves import Move

class GameRenderInfo(object):
    """docstring for GameRenderInfo"""

    def __init__(self):
        self.display_travel = False
        self.display_shop = False
        self.display_loot = True
        self.display_monster = False
        self.display_party = True
        self.display_event = True
        self.display_alter = False
        self.display_info = False
        self.display_options = True
        self.display_background = True
        self.current_menu = None
        self.background = "images/ui/background.png"


class GameMenu(BattleController):
    """View and controller of game"""

    def __init__(self):
        super().__init__()
        # TMP
        players = [Player("Test Player") for i in range(4)]
        self.game = Game(players)
        self.render_info = GameRenderInfo()

        self.background = Image(
            (0,0),
            filename = self.render_info.background,
            h_anchor = 1,
            v_anchor = 1)
        self.background.display()

        self.party_menu = PartyMenu(self.game, self.render_info)
        self.event_menu = None
        self.travel_menu = None
        self.battle_info_menu = None
        self.bars = None
        self.shop_menu = None
        self.loot_menu = None
        self.alter_menu = None
        self.monster_menu = None
        self.sidebar = None

        self.party_menu.display()

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
        self.battle_info_menu = BattleInfoMenu(character, self.cast,
            is_battle, is_limited)
        self.bars.add(self.battle_info_menu.bars)
        self.battle_info_menu.display()

    def cast(self, move):
        target = self.get_target(move)
        move.caster.target = target
        move.caster.cast(move, self.battle)

    def get_target(self, move):
        if move.targeting == "single":
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        return None

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

        if all(m.fallen for m in self.battle.monsters):
            print(True)

        for monster in self.battle.monsters:
            if monster.ready:
                monster.cast("hello", self.battle)

    def set_current_character(self, character):
        self.current_char = character
        self.render_battle_info()