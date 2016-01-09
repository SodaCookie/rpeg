from copy import copy

import pygame

from engine.ui.core.renderable import Renderable
from engine.ui.core.zone import Zone
from engine.ui.core.bindable import Bindable
from engine.ui.element.window import Window
from engine.ui.element.text import Text

class Button(Renderable, Bindable):
    """Clickable Button object. Contains actions for hovering and clicking
    """

    def __init__(self, text, size, x, y, windowed=False):
        super().__init__()
        self.text = text
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
                text.get_height()+SCALE*2, None)
            bg.blit(text, (SCALE*2, SCALE*2))
            return bg
        return text

    def draw_hover(self, text, size, windowed):
        """Draw method when hovered"""
        SCALE = 4
        text = Text.draw(text, size, (255, 255, 0), None, Text.LEFT)
        if windowed:
            bg = Window.draw(text.get_width()+SCALE*2,
                text.get_height()+SCALE*2, (255, 255, 0))
            bg.blit(text, (SCALE*2, SCALE*2))
            return bg
        return text

    def draw_click(self, text, size, windowed):
        """Draw method when clicked"""
        SCALE = 4
        text = Text.draw(text, size, (0, 255, 0), None, Text.LEFT)
        if windowed:
            bg = Window.draw(text.get_width()+SCALE*2,
                text.get_height()+SCALE*2, (0, 255, 0))
            bg.blit(text, (SCALE*2, SCALE*2))
            return bg
        return text

    def render(self, surface, game):
        """Only changes if rendered"""
        if self.bound:
            if self.bound.state == Zone.NEUTRAL:
                surface.blit(self.surface, (self.x, self.y))
            elif self.bound.state == Zone.HOVERED:
                surface.blit(self.hover, (self.x, self.y))
            elif self.bound.state == Zone.CLICKED:
                surface.blit(self.click, (self.x, self.y))
        else:
            surface.blit(self.surface, (self.x, self.y))
