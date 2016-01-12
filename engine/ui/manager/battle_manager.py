"""Defines the BattleManager"""
import pygame

from engine.game.item.item import Item
from engine.ui.core.manager import Manager

class BattleManager(Manager):
    """BattleManager is responsible for the proper updating of the battle
    and at the end of the battle generate loot tables for the party when
    an encounter is complete. """

    def __init__(self):
        super(BattleManager, self).__init__()
        self.in_battle = False
        self.time = pygame.time.get_ticks()

    def update(self, game):
        """Looks for battle indicator in game object"""
        super().update(game)
        if not self.in_battle and game.encounter:
            self.in_battle = True
        if self.in_battle and not game.encounter:
            self.in_battle = False
        if self.in_battle:
            self.update_battle(game)
        self.time = pygame.time.get_ticks()

    def update_battle(self, game):
        """Deals with updating the battle game loop"""
        delta_time = (pygame.time.get_ticks() - self.time)/1000
        # Update player
        for player in game.party.players:
            player.handle_battle(delta_time, game)

        # Update monster
        for monster in game.encounter:
            monster.handle_battle(delta_time, game)

        # Check for win or lose conditions
        if all(player.fallen for player in game.party.players):
            print("LOST")

        if all(monster.fallen for monster in game.encounter):
            # Create loot
            difficulty = sum(m.rating for m in game.encounter)
            # constant for the difficulty of fight
            shards = round(difficulty*0.5)
            experience = round(difficulty*0.3)
            items = [Item() for i in range(len(game.encounter))]
            game.loot = (shards, items)
            game.party.shards += shards
            game.focus_window = "loot"
            # Remove the encounter
            game.encounter = []