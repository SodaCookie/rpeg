import pygame

from engine.ui.core.renderable import Renderable

class Image(Renderable):
    """Basic object to render graphics"""

    def __init__(self, name, x, y, surface):
        super().__init__(name, x, y)
        self.x = x
        self.y = y
        if isinstance(surface, str):
            self.surface = pygame.image.load(surface).convert_alpha()
        else:
            self.surface = surface

    def set_surface(self, surface):
        if isinstance(surface, str):
            self.surface = pygame.image.load(surface).convert_alpha()
        else:
            self.surface = surface

    def render(self, surface, game, system):
        surface.blit(self.surface, (self.x, self.y))