from copy import copy

import pygame

from engine.rendering.core.renderable import Renderable
from engine.rendering.element.window import Window
from engine.rendering.element.text import Text

class Button(Renderable):

    def __init__(self, text, size, x, y, on_click=None, windowed=False):
        self.text = text
        self.on_click = on_click
        self.size = size
        self.x = x
        self.y = y
        self.surface = self.draw(self.text, self.size, windowed)
        self.hover = self.draw_hover(self.text, self.size, windowed)
        self.click = self.draw_click(self.text, self.size, windowed)

    def draw(self, text, size, windowed):
        SCALE = 4
        surface = Text.draw(text, size, (255, 255, 255))

        return surface

    def render(self, surface, game):
        surface.blit(self.surface, (self.x, self.y))