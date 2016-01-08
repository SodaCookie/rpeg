import pygame

from engine.ui.core.renderable import Renderable

class Image(Renderable):

    def __init__(self, image, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.surface = image

    def render(self, surface, game):
        surface.blit(self.surface, (self.x, self.y))
