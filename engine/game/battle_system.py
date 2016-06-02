"""Implements the Battle System"""

import pygame

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
            player.handle_battle(delta_time, game)

        # Update monster
        for monster in game.encounter:
            monster.handle_battle(delta_time, game)

        # Check for win or lose conditions
        if all(player.fallen for player in game.party.players):
            print("LOST")
            self.game.quit()

        if all(monster.fallen for monster in game.encounter):
            for player in game.party.players:
                player.cleanup_battle()

            shards, items = self.generate_loot(game.encounter)
            game.loot = (shards, items)
            game.party.shards += shards
            game.focus_window = "loot"
            # Remove the encounter
            game.encounter = []

    def generate_loot(self, encounter):
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
        if game.encounter:
            self.handle_battle(delta, game)