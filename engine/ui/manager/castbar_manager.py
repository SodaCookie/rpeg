"""Defines the CastbarManager"""
from functools import partial

import pygame

from engine.ui.core.manager import Manager
import engine.ui.element as element


class CastBarManager(Manager):
    """Responsible for managing the castbar of the Player characters in and out
    of battle."""

    def __init__(self, x, y, slots):
        super().__init__("castbar", 0, 0)
        SCALE = 4
        self.character = None
        self.y = y

        # Each slot is of size 56
        window_width = 56 * slots + 14

        self.add_renderable(element.Frame("cast_bar_frame", x, y, window_width, 68))

        self.skill_elements = []
        for i in range(slots):
            skill = element.CastBarSlot("slot-%d" % i, x + 8 + i * 56, y + 7,
                None)
            self.skill_elements.append(skill)
            self.add_renderable(skill)
            self.add_renderable(element.Text("slot-text-%d" % i,
                x + i * 56, y + 40, str(i + 1), 16, width=56,
                justify="right"))

    def set_player(self, player):
        for i, slot in enumerate(self.skill_elements):
            slot.set_new_address((player.castbar, i))

    def render(self, surface, game, system):
        super().render(surface, game, system)

        if game.current_player:
            if game.current_player is not self.character:
                self.set_player(game.current_player)
                self.character = game.current_player
                game.selected_move = None