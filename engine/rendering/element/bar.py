import pygame

from engine.rendering.core.renderable import Renderable

class Bar(Renderable):

    def __init__(self, width, height, colour, x, y):
        self.x = x
        self.y = y
        self.percent = 0
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.surface.fill(colour)

    def render(self, surface, game):
        surface.blit(self.surface, (self.x, self.y),
            (0, 0, round(self.width*percent/100), height))