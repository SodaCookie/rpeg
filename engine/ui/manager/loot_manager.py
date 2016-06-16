"""Defines the Loot Manager"""
from functools import partial
from itertools import zip_longest

import pygame

from engine.ui.core.manager import Manager
import engine.ui.element as element

class LootManager(Manager):
    """Deals with the travel UI when moving through the Dungeon"""

    def __init__(self, x, y, width, height):
        """Travel manager handles the movement"""
        super().__init__("loot", x, y)
        self.width = width
        self.height = height
        self.loot = None
        self.item_elements = []
        self.item_text_elements = []
        self.overflow = []

        # Window
        self.add_renderable(element.Frame("frame", x, y, width,
            height))

        # Slots and slot text
        for i in range(5):
            text = element.Text("item-text-%d" % i, x + 84, y + 36 + i * 60,
                "", 20, width=width - 84)
            slot = element.ItemSlot("item-%d" % i, x + 24, y + 24 + i * 60,
                "any", None)
            slot.on_change = self.update_text(slot, text)
            self.item_elements.append(slot)
            self.item_text_elements.append(text)
            self.add_renderable(slot)
            self.add_renderable(text)

    def update_text(self, slot, text):
        def on_change(game, system):
            if slot.get():
                text.set_text(slot.get().name)
            else:
                text.set_text("")
        return on_change

    def set_items(self, items):
        if items == None:
            return
        self.overflow = []
        for elem, text, i in zip_longest(self.item_elements,
                self.item_text_elements, range(len(items)), fillvalue=None):
            if i is None:
                self.overflow.append(None)
                elem.set_new_address((self.overflow, len(self.overflow) - 1))
                text.set_text("")
            else:
                elem.set_new_address((items, i))
                text.set_text(items[i].name)

    def update(self, game, system):
        if game.loot != self.loot and game.loot is not None:
            self.loot = game.loot
            self.set_items(game.loot[0])