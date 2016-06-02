"""Implements the Game System"""

import pygame

from engine.serialization.move import MoveDataManager

from engine.system import System, Message
from engine.game.dungeon.dungeon import Dungeon
from engine.game.player.player import Player
from engine.game.party.party import Party
from engine.ui.core.manager import Manager

class GameSystem(System):
    """System responsible for handling game related events"""

    def __init__(self, game):
        super().__init__(game, "game")
        self.move_dm = MoveDataManager()

    def init(self, game):
        game.difficulty = "normal"
        game.current_dungeon = Dungeon("catacombs", game.difficulty)
        game.floor_type = game.current_dungeon.level
        game.current_location = game.current_dungeon.start
        game.current_location.generate()
        game.current_dialog = game.current_location.get_event()
        game.focus_window = "scenario"
        game.party = Party([Player("Player "+str(i)) for i in range(3)])
        game.loot = None
        for player in game.party.players:
            player.add_move(self.move_dm.get_move("attack"))
            player.castbar[0] = player.moves[0] # temp

    def handle_events(self, game):
        """Helper function to handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.quit()
                return
        game.mouse_x, game.mouse_y = pygame.mouse.get_pos()
        game.mouse_button = pygame.mouse.get_pressed()

    def update(self, delta, game):
        self.handle_events(game)