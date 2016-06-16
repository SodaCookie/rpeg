import random

import pygame

from engine.system import Message
from engine.ui.core.zone import Zone
from engine.ui.element.abstractbutton import AbstractButton
import engine.ui.draw as draw

class Button(AbstractButton):
    """Implemented AbstractButton to handle nice rendering. Does not
    feature vertical wordwrap"""

    def __init__(self, name, on_click=None, off_click=None, **kwargs):
        defaults = {
            "text" : "",
            "size" : 16,
            "justify" : "center",
            "vjustify" : "center",
            "width" : None,
            "height" : None,
            "x" : 0,
            "y" : 0,
            "windowed" : True,
        }
        defaults.update(kwargs)
        # Set values
        for key, value in defaults.items():
            setattr(self, key, value)

        # Create font
        self.draw_seed = random.randint(0, 100)
        self.font = pygame.font.Font("assets/fonts/VT323-Regular.ttf",
            self.size)

        # Width defaults (width, height > text > None)
        if self.width and self.height:
            # For clarity
            pass
        elif self.text:
            width, height = self.font.size(self.text)
            self.width = width if self.width is None else self.width
            self.height = height if self.height is None else self.height
        else:
            self.width = 100
            self.height = 100

        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        super().__init__(name, rect, on_click, off_click)

    def on_hovered(self, game, system):
        system.message("sound", Message("ui",
                "data/sound/menu_select_sfx.wav"))

    def on_clicked(self, game, system):
        system.message("sound", Message("ui",
                "data/sound/click.wav"))

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_text(self, text):
        """Convenience function that will update the text for the object"""
        self.text = text
        self.set_dirty(True)

    def render_neutral(self, game):
        """Override. Called whenever refresh is called. Expects an image
        to represent the neutral state."""
        # Base if any
        if self.windowed:
            surface = draw.frame.draw_frame(self.width, self.height,
                seed=self.draw_seed)
        else:
            surface = draw.simple.draw_rect(self.width, self.height,
                (0, 0, 0, 0))

        # Text if any
        text = None
        if self.text:
            text = draw.simple.draw_text(self.text, self.font, (255, 255, 255),
                self.width, True, self.justify)

        # Apply text
        if text is not None:
            mid = (surface.get_width() - text.get_width()) // 2
            if self.vjustify == "up":
                surface.blit(text, (mid, 0))
            elif self.vjustify == "center":
                surface.blit(text, (mid,
                    (surface.get_height() - text.get_height()) // 2))
            elif self.vjustify == "down":
                surface.blit(text, (mid,
                    surface.get_height() - text.get_height()))
        return surface

    def render_hover(self, game):
        """Override. Called whenever refresh is called. Expects an image
        to represent the hovered state."""
        if self.windowed:
            surface = draw.frame.draw_highlight_frame(self.width, self.height,
                (255, 255, 0), seed=self.draw_seed)
        else:
            surface = draw.simple.draw_rect(self.width, self.height,
                (0, 0, 0, 0))

        # Text if any
        text = None
        if self.text:
            text = draw.simple.draw_text(self.text, self.font, (255, 255, 0),
                self.width, True, self.justify)

        # Apply text
        if text is not None:
            mid = (surface.get_width() - text.get_width()) // 2
            if self.vjustify == "up":
                surface.blit(text, (mid, 0))
            elif self.vjustify == "center":
                surface.blit(text, (mid,
                    (surface.get_height() - text.get_height()) // 2))
            elif self.vjustify == "down":
                surface.blit(text, (mid,
                    surface.get_height() - text.get_height()))
        return surface

    def render_clicked(self, game):
        """Override. Called whenever refresh is called. Expects an image
        to represent the clicked state."""
        if self.windowed:
            surface = draw.frame.draw_highlight_frame(self.width, self.height,
                (50, 255, 50), seed=self.draw_seed)
        else:
            surface = draw.simple.draw_rect(self.width, self.height,
                (0, 0, 0, 0))

        # Text if any
        text = None
        if self.text:
            text = draw.simple.draw_text(self.text, self.font, (50, 255, 50),
                self.width, True, self.justify)

        # Apply text
        if text is not None:
            mid = (surface.get_width() - text.get_width()) // 2
            if self.vjustify == "up":
                surface.blit(text, (mid, 0))
            elif self.vjustify == "center":
                surface.blit(text, (mid,
                    (surface.get_height() - text.get_height()) // 2))
            elif self.vjustify == "down":
                surface.blit(text, (mid,
                    surface.get_height() - text.get_height()))
        return surface
