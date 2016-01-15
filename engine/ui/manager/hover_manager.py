"""Defines the HoverManager"""
import pygame

from engine.ui.core.manager import Manager
from engine.ui.element.image import Image

class HoverManager(Manager):

    def __init__(self):
        super().__init__()
        self.image = None

    def update(self, game):
        super().update(game)

    def render(self, surface, game):
        if game.current_hover_image != None:
            height = game.current_hover_image.get_height()
            surface.blit(game.current_hover_image,
                (game.mouse_x + game.hover_x,
                 game.mouse_y - height + game.hover_y))
        super().render(surface, game)
