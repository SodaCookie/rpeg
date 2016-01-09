import pygame

from engine.ui.core.renderable import Renderable

class Bar(Renderable):
    """A Bar that is filled a certain amount from 0 - 100%"""

    def __init__(self, width, height, colour, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.percent = 100
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.surface.fill(colour)

    def render(self, surface, game):
        surface.blit(self.surface, (self.x, self.y),
            (0, 0, round(self.width*self.percent/100), self.height))
