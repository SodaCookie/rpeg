from copy import copy

import pygame

from engine.system import Message
from engine.ui.element.abstractbutton import AbstractButton
import engine.ui.draw as draw

class TravelButton(AbstractButton):
    """Implemented AbstractButton to handle nice rendering. Does not
    feature vertical wordwrap"""

    COLOUR = {
        "unknown" : (79, 74, 59),
        "visited" : (255, 255, 255),
        "current" : (255, 255, 0)
    }

    def __init__(self, name, x, y, ntype, location):
        super().__init__(name, (x, y, 33, 33))
        self.ntype = ntype
        self.location = location
        self.visible = False
        self.disable = False

    def on_clicked(self, game, system):
        if not self.disable:
            system.message("sound", Message("ui", "data/sound/click.wav"))

    def on_click(self, game, system):
        if not self.disable:
            system.message("ui", Message("layout", "scenario"))
            system.message("game", Message("travel", self.location))

    def off_click(self, game, system):
        pass

    def set_ntype(self, ntype):
        self.ntype = ntype
        self.set_dirty(True)

    def render(self, surface, game, system):
        if self.visible:
            super().render(surface, game, system)

    def render_neutral(self, game):
        surface = pygame.Surface((11, 11), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        pygame.draw.circle(surface, (195, 193, 187), (4, 4), 4)
        pygame.draw.circle(surface, self.COLOUR[self.ntype], (4, 4), 3)
        surface = pygame.transform.scale(surface, (33, 33))
        return surface

    def render_hover(self, game):
        """Draw method when hovered"""
        if self.disable:
            return self.render_neutral(game)
        surface = pygame.Surface((11, 11), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        pygame.draw.circle(surface, (255, 255, 0), (4, 4), 4)
        pygame.draw.circle(surface, self.COLOUR[self.ntype], (4, 4), 3)
        surface = pygame.transform.scale(surface, (33, 33))
        return surface

    def render_clicked(self, game):
        """Draw method when clicked"""
        if self.disable:
            return self.render_neutral(game)
        surface = pygame.Surface((11, 11), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        pygame.draw.circle(surface, (0, 255, 0), (4, 4), 4)
        pygame.draw.circle(surface, self.COLOUR[self.ntype], (4, 4), 3)
        surface = pygame.transform.scale(surface, (33, 33))
        return surface