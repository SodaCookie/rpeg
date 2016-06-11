"""Implements the UI System"""
from collections import OrderedDict

import pygame

from engine.system import System, Message
import engine.ui.manager as manager

class HoverSystem(System):
    """System responsible for handling game related events"""

    def __init__(self, game):
        super().__init__(game, "hover")
        self.clicked = 0

    def update(self, delta, game):
        messages = self.flush_messages()
        for message in messages:
            self.dispatch(message, game)
        # Check for removing
        if self.clicked != game.mouse_button[0]:
            # Drop
            if self.clicked == 1:
                if game.hover_data is not None:
                    _, slot, _ = game.hover_data
                    game.hover_data = None
                    if slot.dropable:
                        slot.set_address(None)
                    else:
                        slot.set_address(slot.address[0][slot.address[1]])
            self.clicked = game.mouse_button[0]
        # Draw to the screen
        if self.clicked and game.hover_data is not None:
            surface = pygame.display.get_surface()
            x, y = game.mouse_x, game.mouse_y
            pygame.draw.rect(surface, (255, 255, 255), (x-8, y-8, 16, 16))

    def dispatch(self, message, game):
        """Function for determining what action to call depending on the
        message"""
        if message.mtype == "set":
            # Set hovered object from a slot
            game.hover_data = message.args
        elif message.mtype == "drop":
            # Removes the tracked hovered object
            prev = game.hover_data[1]
            other = message.args[0]
            value = prev.address[0][prev.address[1]]
            other_value = other.address[0][other.address[1]]

            # Set values
            other.set_address(value)
            if prev.cloneable and prev.swapable:
                if other_value is not None:
                    prev.set_address(other_value)
            elif prev.cloneable and not prev.swapable:
                pass
            elif not prev.cloneable and prev.swapable:
                prev.set_address(other_value)
            elif not prev.cloneable and not prev.swapable:
                prev.set_address(None)

            # Clear hover data
            game.hover_data = None