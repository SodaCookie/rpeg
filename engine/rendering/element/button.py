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
        text = Text.draw(text, size, (255, 255, 255), None, Text.LEFT)
        if windowed:
            bg = Window.draw(text.get_width()+SCALE*2,
                text.get_height()+SCALE*2)
            bg.blit(surface, (SCALE*2, SCALE*2))
            return bg
        return text

    def draw_hover(self, text, size, windowed):
        SCALE = 4
        text = Text.draw(text, size, (255, 255, 0), None, Text.LEFT)
        if windowed:
            bg = Window.draw(text.get_width()+SCALE*2,
                text.get_height()+SCALE*2)
            bg.fill((255, 255, 0), (0, 0, SCALE, bg.get_height()))
            bg.fill((255, 255, 0), (0, 0, bg.get_width(), SCALE))
            bg.fill((255, 255, 0),
                (bg.get_width()-SCALE, 0, SCALE, bg.get_height()))
            bg.fill((255, 255, 0),
                (0, bg.get_height()-SCALE, bg.get_width(), SCALE))
            bg.fill((0, 0, 0, 0), (0, 0, SCALE*2, SCALE*2))
            bg.fill((0, 0, 0, 0),
                (0, bg.get_height()-SCALE*2, SCALE*2, SCALE*2))
            bg.fill((0, 0, 0, 0),
                (bg.get_width()-SCALE*2, 0, SCALE*2, SCALE*2))
            bg.fill((0, 0, 0, 0),
                (bg.get_width()-SCALE*2, bg.get_height()-SCALE*2, SCALE*2, SCALE*2))
            bg.fill((255, 255, 0), (SCALE*2, SCALE*2, SCALE, SCALE))
            bg.fill((255, 255, 0),
                (SCALE*2, bg.get_height()-SCALE*2, SCALE, SCALE))
            bg.fill((255, 255, 0),
                (bg.get_width()-SCALE*2, 0, SCALE, SCALE))
            bg.fill((255, 255, 0),
                (bg.get_width()-SCALE*2, bg.get_height()-SCALE*2, SCALE, SCALE))
            bg.blit(surface, (SCALE*2, SCALE*2))
            return bg
        return text

    def draw_click(self, text, size, windowed):
        SCALE = 4
        text = Text.draw(text, size, (255, 255, 255), None, Text.LEFT)
        if windowed:
            bg = Window.draw(text.get_width()+SCALE*2,
                text.get_height()+SCALE*2)
            bg.fill((0, 255, 0), (0, 0, SCALE, bg.get_height()))
            bg.fill((0, 255, 0), (0, 0, bg.get_width(), SCALE))
            bg.fill((0, 255, 0),
                (bg.get_width()-SCALE, 0, SCALE, bg.get_height()))
            bg.fill((0, 255, 0),
                (0, bg.get_height()-SCALE, bg.get_width(), SCALE))
            bg.fill((0, 0, 0, 0), (0, 0, SCALE*2, SCALE*2))
            bg.fill((0, 0, 0, 0),
                (0, bg.get_height()-SCALE*2, SCALE*2, SCALE*2))
            bg.fill((0, 0, 0, 0),
                (bg.get_width()-SCALE*2, 0, SCALE*2, SCALE*2))
            bg.fill((0, 0, 0, 0),
                (bg.get_width()-SCALE*2, bg.get_height()-SCALE*2, SCALE*2, SCALE*2))
            bg.fill((0, 255, 0), (SCALE*2, SCALE*2, SCALE, SCALE))
            bg.fill((0, 255, 0),
                (SCALE*2, bg.get_height()-SCALE*2, SCALE, SCALE))
            bg.fill((0, 255, 0),
                (bg.get_width()-SCALE*2, 0, SCALE, SCALE))
            bg.fill((0, 255, 0),
                (bg.get_width()-SCALE*2, bg.get_height()-SCALE*2, SCALE, SCALE))
            bg.blit(surface, (SCALE*2, SCALE*2))
            return bg
        return text

    def render(self, surface, game):
        surface.blit(self.surface, (self.x, self.y))