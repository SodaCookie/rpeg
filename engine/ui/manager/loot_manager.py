"""Defines the Loot Manager"""
from functools import partial

import pygame

from engine.ui.core.zone import Zone
from engine.ui.core.manager import Manager
import engine.ui.element as element

class LootManager(Manager):
    """Manager for rendering and handling loot"""

    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.loot = None

    def draw(self):
        self.zones = []
        self.renderables = []
        if not self.loot:
            return

        shard, items = self.loot
        self.items = [items[j] if j < len(items) else None for j in range(5)]
        window = element.Window(self.width, self.height, self.x, self.y)
        title = element.Text("Loot", 30, 0, self.y+10)
        title.x = self.x+self.width//2-title.surface.get_width()//2
        self.renderables.append(window)
        self.renderables.append(title)

        shard_text = element.Text("Shards Earned:", 20, self.x+20,
            self.y+50, width=self.width-40)
        shard_amt_text = element.Text(str(shard), 20, self.x+20, self.y+50,
            width=self.width-40, justify=element.Text.RIGHT)

        self.renderables.append(shard_text)
        self.renderables.append(shard_amt_text)

        for i, item in enumerate(self.items):
            slot = element.Slot(item, "item", self.x+20, self.y+100+60*i,
                self.items, i, False)
            text = item.name if item else ""
            item_name = element.Text(text, 18, self.x+80, self.y+100+60*i,
                width=self.width-100)
            self.renderables.append(slot)
            self.renderables.append(item_name)

        close = element.Button("CLOSE", 30, 0, self.y+self.height+20, True)
        close.x = self.x+self.width//2-close.surface.get_width()//2
        self.renderables.append(close)

    def render(self, surface, game):
        if game.loot and game.focus_window == "loot":
            super().render(surface, game)

    def update(self, game):
        if game.loot and game.focus_window == "loot":
            if self.loot != game.loot:
                self.loot = game.loot
                self.draw()
            super().update(game)