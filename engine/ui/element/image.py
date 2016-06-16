import pygame

from engine.ui.core.renderable import Renderable
from engine.ui.draw.simple import draw_image

class Image(Renderable):
    """Basic object to render graphics"""

    def __init__(self, name, x, y, surface, scale=1):
        super().__init__(name, x, y)
        self.x = x
        self.y = y
        if isinstance(surface, str):
            self.surface = draw_image(surface, scale)
        else:
            self.surface = surface

    def get_size(self):
        return self.surface.get_size()

    def get_width(self):
        return self.surface.get_width()

    def get_height(self):
        return self.surface.get_height()

    def set_surface(self, surface, scale=1):
        if isinstance(surface, str):
            self.surface = draw_image(surface, scale)
        else:
            self.surface = surface

    def render(self, surface, game, system):
        surface.blit(self.surface, (self.x, self.y))