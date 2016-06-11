import pygame

from engine.ui.element.image import Image
from engine.ui.draw.frame import draw_frame

class Frame(Image):
    """Frame Object to contain menus with buttons, slots etc."""

    def __init__(self, name, x, y, width, height):
        surface = draw_frame(width, height)
        super().__init__(name, x, y, surface)
        self.width = width
        self.height = height

