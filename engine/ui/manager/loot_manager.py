"""Defines the Loot Manager"""
from functools import partial

import pygame

from engine.ui.core.zone import Zone
from engine.ui.core.manager import Manager
import engine.ui.element as element

class LootManager(Manager):
    """Manager for rendering and handling loot"""

    def __init__(self):
        pass

    def render(self, surface, game):
        if game.loot and game.focus_window == "loot":
            super().render(surface, game)

    def update(self, game):
        if game.loot and game.focus_window == "loot":
            super().update(game)