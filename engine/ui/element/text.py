import pygame

from engine.ui.element.image import Image
from engine.ui.draw.simple import draw_text

class Text(Image):
    """Text object for displaying strings."""

    def __init__(self, name, x, y, text, size, colour=pygame.Color("white"),
            width=None, justify="left"):
        self.font = pygame.font.Font("assets/fonts/VT323-Regular.ttf",
            size)
        surface = draw_text(text, self.font, colour,
            width, True, justify)
        super().__init__(name, x, y, surface)
        self.text = text
        self.size = size
        self.dirty = False
        self.colour = colour
        self.width = width
        self.justify = justify

    def set_dirty(self, dirty):
        self.dirty = dirty

    def set_text(self, text):
        """Convenience function that will update the text for the object"""
        self.text = text
        self.set_surface(draw_text(self.text, self.font, self.colour,
            self.width, True, self.justify))

    def refresh(self, game):
        self.set_surface(draw_text())

    def render(self, surface, game, system):
        if self.dirty:
            self.refresh(game)
        super().render(surface, game, system)
