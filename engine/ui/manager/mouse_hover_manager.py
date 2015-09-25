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

    def update(self, game):

        if game.current_object and not game.mouse_button[0]:
            game.current_slot.value = game.current_object
            game.current_slot.surface = Slot.draw(game.current_slot.value)
            game.current_slot.hover = Slot.draw_highlight(game.current_slot.value)
            game.current_hover = None
            game.current_object = None
            game.current_slot = None


    def render(self, surface, game):
        if game.current_hover:
            surface.blit(game.current_hover, (game.mouse_x + game.hover_x, game.hover_y + game.mouse_y))