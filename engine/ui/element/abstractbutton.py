"""Implements the abstract button class"""
import pygame

from engine.ui.core.zone import Zone
from engine.ui.core.renderable import Renderable

class AbstractButton(Renderable):
    """AbstractButton defines an abstract button which doesn't implement
    'rendering' but does implement the pressing of a button and what states
    can be rendered."""

    def __init__(self, name, rect, on_click=None, off_click=None):
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
        if on_click is not None:
            self.on_click = on_click
        if off_click is not None:
            self.off_click = off_click

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

    def on_click(self, game, system):
        """Override. Called whenever the button is clicked"""
        pass

    def off_click(self, game, system):
        """Override. Called whenever the button is unclicked"""
        pass

    def render_neutral(self, game):
        """Override. Called whenever refresh is called. Expects an image
        to represent the neutral state."""
        return None

    def render_hover(self, game):
        """Override. Called whenever refresh is called. Expects an image
        to represent the hovered state."""
        return None

    def render_clicked(self, game):
        """Override. Called whenever refresh is called. Expects an image
        to represent the clicked state."""
        return None

    def refresh(self, game):
        """Redraws all relevant images for the button"""
        self.neutral = self.render_neutral(game)
        self.hover = self.render_hover(game)
        self.clicked = self.render_clicked(game)

    def render(self, surface, game, system):
        if self.dirty:
            self.refresh(game)
            self.dirty = False

        prev_state = self.zone.state
        self.zone.update(game)

        # Handling
        if self.zone.state == Zone.CLICKED and prev_state != Zone.CLICKED:
            self.on_click(game, system)
        elif self.zone.state == Zone.HOVERED and prev_state == Zone.CLICKED:
            self.off_click(game, system)

        # Rendering
        if self.zone.state == Zone.NEUTRAL:
            button_surf = self.neutral
        elif self.zone.state == Zone.HOVERED:
            button_surf = self.hover
        elif self.zone.state == Zone.CLICKED:
            button_surf = self.clicked

        if button_surf is not None:
            surface.blit(button_surf, (self.x, self.y))