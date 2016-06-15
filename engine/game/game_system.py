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
        self.message(Message("travel", game.current_dungeon.start))
        game.party = Party([Player("Player "+str(i+1)) for i in range(4)])
        game.loot = None
        for player in game.party.players:
            if player is not None:
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
        messages = self.flush_messages()
        for message in messages:
            self.dispatch(message, game, self.game)

    def dispatch(self, message, game, system):
        """Function for determining what action to call depending on the
        message"""
        if message.mtype == "travel": # Travels the part
            location = message.args[0]
            game.current_location = location
            game.current_location.generate()
            game.current_dialogue = game.current_location.get_event()
            game.loot = None
        elif message.mtype == "choice":
            dialogue = message.args[0]
            game.current_dialogue = dialogue
        elif message.mtype == "action":
            dialogue = message.args[0]
            for action in dialogue.get_actions():
                action.execute(game, system)
        elif message.mtype == "close-event":
            game.current_dialogue = None
            game.current_player = None
        elif message.mtype == "select-player":
            player = message.args[0]
            game.current_player = player
        elif message.mtype == "loot":
            items, shards = message.args
            game.loot = (shards, items)
            game.party.shards += shards
