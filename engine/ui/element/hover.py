"""Implements the abstract Hover class"""
import pygame

from engine.ui.core.zone import Zone
from engine.ui.core.renderable import Renderable

class Hover(Renderable):
    """Hover defines an interface which doesn't implement
    'rendering' but does implements the hovering part of a zone."""

    def __init__(self, name, rect, on_hover=None, off_hover=None):
        # Normalize rect data
        rect = pygame.Rect(rect)

        # Initialize
        super().__init__(name, rect.x, rect.y)
        self.zone = Zone(rect)
        self.dirty = True
        self.neutral = None
        self.hover = None
        self.clicked = None

        # Set on click
        if on_hover is not None:
            self.on_hover = on_hover
        if off_hover is not None:
            self.off_hover = off_hover

    def move(self, x, y):
        """Moves the renderable to new location"""
        super().move(x, y)
        self.rect.x = x
        self.rect.y = y
        self.update_rect(self.rect)

    def set_size(self, width, height):
        self.rect.w = width
        self.rect.h = height
        self.update_rect(self.rect)

    def set_dirty(self, dirty):
        self.dirty = dirty

    def on_hover(self, game, system):
        """Override. Called whenever the hover is hovered over"""
        pass

    def off_hover(self, game, system):
        """Override. Called whenever the button is hovered off"""
        pass

    def render(self, surface, game, system):
        if self.dirty:
            self.refresh(game)
            self.dirty = False

        prev_state = self.zone.state
        self.zone.update(game)

        # Handling
        if self.zone.state != Zone.NEUTRAL and prev_state == Zone.NEUTRAL:
            self.on_hover(game, system)
        elif self.zone.state == Zone.NEUTRAL and prev_state != Zone.NEUTRAL:
            self.off_hover(game, system)