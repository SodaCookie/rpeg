"""Defines the character renderer."""
import random
import logging

import pygame

from engine.system import Message

from engine.ui.element.abstractbutton import AbstractButton
from engine.ui.element.bar import PercentBar
import engine.ui.draw.frame as frame
import engine.ui.draw.simple as simple

class MonsterCard(AbstractButton):
    """Manager for the character class"""

    def __init__(self, name, x, y, monster):
        super().__init__(name, (x, y, 240, 156))
        self.font = pygame.font.Font("assets/fonts/VT323-Regular.ttf",
            20)
        self.monster = monster
        self.base_x = x
        self.base_y = y
        self.health = PercentBar("player-health", x, y + 8, simple.draw_rect(160, 8, (50, 255, 50)))
        self.action = PercentBar("player-action", x, y + 20, simple.draw_rect(160, 8, (50, 100, 50)))

    def on_hovered(self, game, system):
        system.message("sound", Message("ui",
                "data/sound/menu_select_sfx.wav"))

    def set_monster(self, monster):
        self.monster = monster
        self.set_dirty(True)

    def on_click(self, game, system):
        if game.current_player and game.current_player.selected_move and \
                not self.monster.fallen:
            if game.current_player.selected_move.is_valid_target(
                    game.current_player.target+[self.monster],
                    game.party.players,
                    game.encounter):
                system.message("battle", Message("select-target",
                    self.monster))

    def refresh(self, game):
        super().refresh(game)
        if self.neutral is not None:
            self.x = self.base_x - self.neutral.get_width() // 2
            self.y = self.base_y - self.neutral.get_height()
            self.rect.x = self.x
            self.rect.y = self.y + 30
            self.set_size(self.neutral.get_width(),
                          self.neutral.get_height() - 30)
        self.health.move(self.x + self.rect.w // 2 - 80 , self.base_y + 8)
        self.action.move(self.x + self.rect.w // 2 - 80 ,
            self.base_y + 20)

    def move(self, x, y):
        super().move(x, y)
        self.base_x = x
        self.base_y = y

    def render_neutral(self, game):
        surface = None
        monster_image = None
        if self.monster:
            if self.monster.graphic.get("neutral"):
                try:
                    filename = self.monster.graphic.get("neutral")
                    monster_image = simple.draw_image(filename, 4)
                except pygame.error:
                    monster_image = simple.draw_rect(240, 80, (255, 255, 255))
                    logging.warning("Could not load: " + filename)
            else:
                monster_image = simple.draw_rect(240, 80, (255, 255, 255))
            surface = pygame.Surface((monster_image.get_width(),
                monster_image.get_height() + 30), pygame.SRCALPHA)
            surface.fill((0, 0, 0, 0))
            surface.blit(monster_image, (0, 30))
            surface.blit(simple.draw_text(self.monster.name, self.font,
                (255, 255, 255), surface.get_width(), justify="center"),
                (0, 0))
        return surface

    def render_hover(self, game):
        surface = None
        monster_image = None
        if self.monster:
            if self.monster.graphic.get("hover"):
                try:
                    filename = self.monster.graphic.get("hover")
                    monster_image = simple.draw_image(filename, 4)
                except pygame.error:
                    monster_image = simple.draw_rect(240, 80, (255, 255, 0))
                    logging.warning("Could not load: " + filename)
            else:
                monster_image = simple.draw_rect(240, 80, (255, 255, 0))
            surface = pygame.Surface((monster_image.get_width(),
                monster_image.get_height() + 30), pygame.SRCALPHA)
            surface.fill((0, 0, 0, 0))
            surface.blit(monster_image, (0, 30))
            surface.blit(simple.draw_text(self.monster.name, self.font,
                (255, 255, 0), surface.get_width(), justify="center"),
                (0, 0))
        return surface

    def render_clicked(self, game):
        return self.render_neutral(game)

    def render(self, surface, game, system):
        if self.monster is not None:
            super().render(surface, game, system)
            self.health.set_percent(self.monster.get_cur_health() / \
                self.monster.get_stat("health"))
            self.action.set_percent(self.monster.get_cur_action() / \
                self.monster.get_stat("action"))
            self.health.render(surface, game, system)
            self.action.render(surface, game, system)