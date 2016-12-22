"""Implements the Battle System"""

import pygame

from engine.game.item.item_factory import ItemFactory
from engine.system import System, Message

class BattleSystem(System):
    """System responsible for handling battle"""

    def __init__(self, game):
        super().__init__(game, "battle")

    def handle_battle(self, delta, game):
        """Deals with updating the battle game loop"""
        delta_time = delta/1000
        # Update player
        for player in game.party.players:
            player.handle_battle(delta_time, game, self.game)

        # Update monster
        for monster in game.encounter:
            monster.handle_battle(delta_time, game, self.game)

        # Check for win or lose conditions
        if all(player.fallen for player in game.party.players):
            print("LOST")
            self.game.quit()

        if all(monster.fallen for monster in game.encounter):
            for player in game.party.players:
                player.cleanup_battle()
            shards, items = self.generate_loot(game)
            # Remove the encounter
            self.game.message("battle", Message("end"))
            self.game.message("sound", Message("bg",
                "data/sound/background/Puzzle-Game.wav"))
            if not game.current_dialogue:
                self.game.message("ui", Message("layout", "loot"))
                self.game.message("game", Message("loot", items, shards))
            else:
                self.game.message("ui", Message("layout", "scenario"))

    def generate_loot(self, game):
        # Create loot
        difficulty = sum(m.rating for m in game.encounter)

        # constant for the difficulty of fight
        shards = round(difficulty*0.5)
        experience = round(difficulty*0.3)
        items = [ItemFactory.generate(game.encounter, game.floor_type)
            for i in range(len(game.encounter))]
        loot = (shards, items)
        return loot

    def update(self, delta, game):
        messages = self.flush_messages()
        for message in messages:
            self.dispatch(message, game, self.game)
        if game.encounter:
            self.handle_battle(delta, game)

    def dispatch(self, message, game, system):
        """Function for determining what action to call depending on the
        message"""
        if message.mtype == "start": # Starts the battle
            game.encounter = message.args[0]
        elif message.mtype == "end":
            game.encounter = None
        elif message.mtype == "select-move":
            move = message.args[0]
            game.current_player.selected_move = move
        elif message.mtype == "deselect-move":
            if game.current_player:
                game.current_player.selected_move = None
        elif message.mtype == "select-target":
            if game.current_player:
                character = message.args[0]
                game.current_player.target.append(character)
        elif message.mtype == "clear-selection":
            if game.current_player:
                game.current_player.target = []
