from functools import partial

import pygame

from engine.ui.core.manager import Manager
import engine.ui.element as element

class SideBarManager(Manager):
    """Manages the side bars"""

    def __init__(self, x, y, width):
        super().__init__("sidebar", x, y)

        # Loot
        self.loot_button = element.Button("loot",
            text = "Loot",
            size = 20,
            x = x + width // 2 - 170,
            y = y,
            width = 100,
            height = 50)

        # Travel
        self.travel_button = element.Button("travel",
            text = "Travel",
            size = 20,
            x = x + width // 2 - 50,
            y = y,
            width = 100,
            height = 50)

        # Shop
        self.shop_button = element.Button("shop",
            text = "Shop",
            size = 20,
            x = x + width // 2 + 70,
            y = y,
            width = 100,
            height = 50)

    def render(self, surface, game, system):
        if game.loot is not None:
            self.loot_button.render(surface, game, system)
        if game.current_location and game.current_location.room_type == "shop":
            self.shop_button.render(surface, game, system)
        self.travel_button.render(surface, game, system)
