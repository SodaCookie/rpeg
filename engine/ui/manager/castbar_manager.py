"""Defines the CastbarManager"""
from functools import partial

import pygame

from engine.ui.core.zone import Zone
from engine.ui.core.manager import Manager
import engine.ui.element as element

class CastBarManager(Manager):

    def __init__(self, y):
        super().__init__()
        SCALE = 4
        self.character = None
        self.y = y

        window_width = 566
        window_x = pygame.display.get_surface().get_width()//2-window_width//2-SCALE
        self.renderables.append(element.Window(window_width, 60, window_x, y))
        self.skills = [None for i in range(10)]
        for i in range(1, 11):
            skill = element.MoveIcon(None, 8+window_x+(i-1)*56, y+7)
            self.skills[i-1] = skill
            self.renderables.append(skill)
            self.renderables.append(element.Text(str(i)[-1], 16, 50+window_x+(i-1)*56, y+40))
            on_click = partial(self.on_click, skill)
            zone = Zone(((8+window_x+(i-1)*56, y+7),
                skill.surface.get_size()), on_click)
            skill.bind(zone)
            self.zones.append(zone)

    @staticmethod
    def on_click(move_icon, game):
        game.selected_move = move_icon.move

    def update(self, game):
        super().update(game)
        if game.selected_player is not self.character:
            self.swap_charactor(game.selected_player)
            self.character = game.selected_player

    def swap_charactor(self, character):
        SCALE = 4
        if character:
            for i, move in enumerate(character.castbar):
                self.skills[i].move = move
                self.skills[i].surface = element.MoveIcon.draw(move)
                self.skills[i].hover = element.MoveIcon.draw_highlight(move)
        else:
            for i in range(10):
                self.skills[i].move = None
                self.skills[i].surface = element.MoveIcon.draw(None)
                self.skills[i].hover = element.MoveIcon.draw_highlight(None)

