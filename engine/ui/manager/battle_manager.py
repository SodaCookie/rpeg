"""Defines the BattleManager"""
import pygame

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
        super().update(game)
        if not self.in_battle and game.encounter:
            self.in_battle = True
        if self.in_battle and not game.encounter:
            self.in_battle = False
        if self.in_battle:
            self.update_battle(game)
        self.time = pygame.time.get_ticks()

    def update_battle(self, game):
        delta_time = (pygame.time.get_ticks() - self.time)/1000
        # Cast move is any
        if game.selected_player and game.selected_move and \
                game.selected_target:
            game.selected_move.cast(game.selected_target,
                game.selected_player, game.party, game.encounter)
            game.selected_move = None
            game.selected_player = None
            game.selected_target = None
        # Update player
        for player in game.party:
            player.handle_battle(delta_time)
        # Update monster
        for monster in game.encounter:
            monster.handle_battle(delta_time)
        # Check for win or lose conditions
        if all(player.fallen for player in game.party):
            print("LOST")
        if all(monster.fallen for monster in game.encounter):
            game.encounter = []
