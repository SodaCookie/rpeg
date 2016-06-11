from functools import partial

import pygame

from engine.ui.core.zone import Zone
from engine.ui.core.manager import Manager
import engine.ui.element as element

class SidebarManager(Manager):
    """Manages the side bars"""

    def __init__(self):
        super().__init__()
        # Parameters
        button_width = 100
        button_height = 30
        width = pygame.display.get_surface().get_width()
        height = pygame.display.get_surface().get_height()

        # Stored window surfaces
        self.window_neutral = element.Window.draw(button_width,
            button_height, None)
        self.window_hover = element.Window.draw(button_width,
            button_height, (255, 255, 0))
        self.window_click = element.Window.draw(button_width,
            button_height, (0, 255, 0))

        # Create travel window
        self.travel_window = element.Window(button_width, button_height,
            width-button_width-28, 20)
        self.travel_button = element.Button("Travel", 20, 0, 0)

        # Set text location
        self.travel_button.x = width-(button_width+8)//2-20-\
            self.travel_button.surface.get_width()//2
        self.travel_button.y = self.travel_window.y+(button_height+8)//2-\
            self.travel_button.surface.get_height()//2

        # Create bindings
        on_click = partial(self.on_click, self.travel_window, "travel")
        on_hover = partial(self.on_hover, self.travel_window)
        off_hover = partial(self.off_hover, self.travel_window)
        off_click = partial(self.off_click, self.travel_window)
        self.travel_zone = Zone(((self.travel_window.x, self.travel_window.y),
            self.travel_window.surface.get_size()), on_click, on_hover,
            off_hover, off_click)
        self.travel_button.bind(self.travel_zone)

        # Create loot window
        self.loot_window = element.Window(button_width, button_height,
            width-128, 75)
        self.loot = element.Button("Loot", 20, 0, 0)

        # Set text location
        self.loot.x = width-(button_width+8)//2-20-\
            self.loot.surface.get_width()//2
        self.loot.y = self.loot_window.y+(button_height+8)//2-self.loot.surface.get_height()//2

        # Create bindings
        on_click = partial(self.on_click, self.loot_window, "loot")
        on_hover = partial(self.on_hover, self.loot_window)
        off_hover = partial(self.off_hover, self.loot_window)
        off_click = partial(self.off_click, self.loot_window)
        self.loot_zone = Zone(((self.loot_window.x, self.loot_window.y), self.loot_window.surface.get_size()), on_click, on_hover, off_hover, off_click)
        self.loot.bind(self.loot_zone)

        # Create shop window
        self.shop_window = element.Window(button_width, button_height,
            width-128, 130)
        self.shop = element.Button("Shop", 20, 0, 0)
        self.shop.x = width-(button_width+8)//2-20-self.shop.surface.get_width()//2
        self.shop.y = self.shop_window.y+(button_height+8)//2-self.shop.surface.get_height()//2
        on_click = partial(self.on_click, self.shop_window, "shop")
        on_hover = partial(self.on_hover, self.shop_window)
        off_hover = partial(self.off_hover, self.shop_window)
        off_click = partial(self.off_click, self.shop_window)
        self.shop_zone = Zone(((self.shop_window.x, self.shop_window.y), self.shop_window.surface.get_size()), on_click, on_hover, off_hover, off_click)
        self.shop.bind(self.shop_zone)

        # Create gold window
        self.shards = 0
        self.shard_window = element.Window(button_width, button_height,
            width-128, 185)
        self.shard_text = element.Text("0", 20, width-128, 190,
            width=button_width, justify=element.Text.CENTER)

    def render(self, surface, game):
        self.update(game)
        if not game.encounter:
            if not game.current_dialog:
                self.travel_window.render(surface, game)
                self.travel_button.render(surface, game)
                if game.loot:
                    self.loot_window.render(surface, game)
                    self.loot.render(surface, game)
                if game.shop:
                    self.shop_window.render(surface, game)
                    self.shop.render(surface, game)
            self.shard_window.render(surface, game)
            self.shard_text.render(surface, game)

    def update(self, game):
        if game.party.shards != self.shards:
            self.shard_text.set_text(str(game.party.shards))
            self.shards = game.party.shards
        if not game.encounter and not game.current_dialog:
            self.travel_zone.update(game)
            if game.loot:
                self.loot_zone.update(game)
            if game.shop:
                self.shop_zone.update(game)

    def on_hover(self, window, game):
        window.surface = self.window_hover

    def off_hover(self, window, game):
        window.surface = self.window_neutral

    def on_click(self, window, focus, game):
        window.surface = self.window_click
        if game.focus_window == focus:
            game.focus_window = None
        else:
            game.focus_window = focus

    def off_click(self, window, game):
        window.surface = self.window_hover