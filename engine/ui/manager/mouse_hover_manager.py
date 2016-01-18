import pygame

import engine.game as Game
from engine.ui.core.manager import Manager
import engine.ui.core.zone as Zone
from engine.ui.element.slot import Slot


class MouseHoverManager(Manager):
    """Handles surfaces that should be drawn when mouse is
    hovered over specific zones"""

    def __init__(self):
        super().__init__()
        self.cur = None
        self.counter = 0 # We keep every current_object an additional frame

    def update(self, game):
        if game.current_object and not game.mouse_button[0]:
            self.counter += 1
            if self.counter % 2 == 0:
                if game.current_slot.remove:
                    game.current_slot.value = None
                    game.current_slot.container[game.current_slot.key] = None
                else:
                    game.current_slot.value = game.current_object
                    game.current_slot.container[game.current_slot.key] = \
                        game.current_object # MAYBE
                    if game.current_slot.bound.off_click:
                        game.current_slot.bound.off_click(game) # THE ZONE
                self.counter = 0
        else:
            self.counter = 0


    def render(self, surface, game):
        if game.current_hover:
            surface.blit(game.current_hover, (game.mouse_x + game.hover_x, game.hover_y + game.mouse_y))