import pygame

from engine.ui.core.renderable import Renderable
from engine.ui.core.bindable import Bindable
from engine.ui.core.zone import Zone

class TravelNode(Renderable, Bindable):
    """Node object for displaying travel path/options."""

    COLOUR = {
        "unknown" : (79, 74, 59),
        "visited" : (255, 255, 255),
        "current" : (255, 255, 0)
    }

    def __init__(self, type, x, y, active=False):
        super().__init__()
        self.type = type
        self.x = x
        self.y = y
        self.surface = self.draw_click(type) if active else self.draw(type)
        self.hover = self.draw_hover(type)
        self.click = self.draw_click(type)

    @classmethod
    def draw(self, type):
        SCALE = 3
        surface = pygame.Surface((11, 11), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        pygame.draw.circle(surface, (195, 193, 187), (4, 4), 4)
        pygame.draw.circle(surface, TravelNode.COLOUR[type], (4, 4), 3)
        surface = pygame.transform.scale(surface, (11*SCALE, 11*SCALE))
        return surface

    @classmethod
    def draw_hover(self, type):
        """Draw method when hovered"""
        SCALE = 3
        surface = pygame.Surface((11, 11), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        pygame.draw.circle(surface, (255, 255, 0), (4, 4), 4)
        pygame.draw.circle(surface, TravelNode.COLOUR[type], (4, 4), 3)
        surface = pygame.transform.scale(surface, (11*SCALE, 11*SCALE))
        return surface

    @classmethod
    def draw_click(self, type):
        """Draw method when clicked"""
        SCALE = 3
        surface = pygame.Surface((11, 11), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        pygame.draw.circle(surface, (0, 255, 0), (4, 4), 4)
        pygame.draw.circle(surface, TravelNode.COLOUR[type], (4, 4), 3)
        surface = pygame.transform.scale(surface, (11*SCALE, 11*SCALE))
        return surface

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
