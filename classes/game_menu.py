import random

import pygame

import classes.rendering.view as view
from classes.party_menu import PartyMenu
from classes.event_menu import EventMenu
from classes.option_menu import OptionMenu
from classes.travel_menu import TravelMenu
from classes.battle_info_menu import BattleInfoMenu
from classes.loot_menu import LootMenu
from classes.monster_menu import MonsterMenu
from classes.bars import Bars
from classes.image_cache import ImageCache
from classes.rendering.dragable import Dragable
from classes.rendering.image import Image
from classes.rendering.text import Text, TextInfo
from classes.rendering.button import Button, ButtonInfo
from classes.controller import BattleController, MouseController

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
        self.display_option = True
        self.display_background = True
        self.background = "images/ui/background.png"


class GameMenu(BattleController, MouseController, view.Renderable):
    """View and controller of game"""

    def __init__(self):
        MouseController.__init__(self)
        BattleController.__init__(self)
        view.Renderable.__init__(self, (0, 0))
        # TMP
        players = [Player("Test Player") for i in range(4)]
        self.game = Game(players)
        self.render_info = GameRenderInfo()

        self.party_menu = PartyMenu(self.game, self.render_info)
        self.event_menu = EventMenu(self.game, self.render_info)
        self.option_menu = OptionMenu(self.game, self.render_info)
        self.travel_menu = TravelMenu(self.game, self.render_info)
        self.battle_info_menu = BattleInfoMenu(self.game, self.render_info)
        self.monster_menu = MonsterMenu(self.game, self.render_info)
        self.shop_menu = None
        self.loot_menu = None
        self.alter_menu = None

        self.generate_dungeon()

        self.display()  # for background
        self.party_menu.display()
        self.event_menu.display()
        self.option_menu.display()
        self.travel_menu.display()
        self.battle_info_menu.display()
        self.monster_menu.display()

    def delete(self):
        MouseController.delete(self)
        BattleController.delete(self)
        view.Renderable.delete(self)

    def generate_dungeon(self, level_type=None, power=None, **kwargs):
        if level_type == None:
            level_type = random.choice(Game.DUNGEON_TYPES)
        if power == None:
            power = self.game.level * Game.POWER_PER_LEVEL
        self.game.dungeon = Dungeon(level_type, power,
            self.game.difficulty, **kwargs)
        self.game.current_location = self.game.dungeon.start
        self.game.current_location.generate()
        self.game.current_event = self.game.current_location.get_event()

    def handle_battle(self, delta):
        pass

    def draw(self, screen):
        screen.blit(ImageCache.add(self.render_info.background), (0, 0))

        if self.game.current_move:
            # Have a move that requires mouse
            if self.game.current_move.cast_type in ["single", "group"]:
                pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)

    def mouse_button_down(self, button, pos):
        """In charge of actual move casting"""
        if self.game.current_move:
            if button == 3: # RIGHT CLICK
                self.game.current_move = None
            elif button == 1:
                if self.game.hover_character:
                    if self.game.current_move.cast_type in ["single"]:
                        self.game.current_move.caster.target = self.game.hover_character
                        print(self.game.current_move.caster)
                        self.game.current_move.caster.cast(self.game.battle, self.game.current_move)
                    elif self.game.current_move.cast_type in ["group"]:
                        self.game.current_move.caster.target = self.game.hover_character
                        self.game.current_move.caster.cast(self.game.battle, self.game.current_move)
                    self.game.current_move = None
