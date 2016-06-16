import pygame

from engine.ui.draw.simple import draw_rect
from engine.ui.core.manager import Manager
import engine.ui.element as element

class PartyInfoManager(Manager):
    """Manages the rendering of the character card ui and all
    relevant variables and updates (inventory, moves, etc.)"""

    def __init__(self, x, y, width, height, game):
        super().__init__("party-info", x, y)

        # Frame
        self.add_renderable(element.Frame("frame", x, y, width,
            height))

        # Shards
        self.add_renderable(element.Text("shard-text", x + 12,
            y + 12, "Shards: ", 20, width=width-24, justify="left"))
        self.shard_element = element.Text("shard-amount", x + 12,
            y + 12, "", 20, width=width-24, justify="right")
        self.add_renderable(self.shard_element)

        # Item slots
        self.item_elements = []
        item_x = x + 12
        item_y = y + 100
        self.add_renderable(element.Text("inventory-text", item_x + 4,
            item_y - 32, "Party Inventory", 24, width=180, justify="left"))
        for i in range(16):
            item_element = element.ItemSlot("item-slot-%d" % i,
                item_x + (i % 4) * 60, item_y + (i // 4) * 60, "any",
                (game.party.inventory, i))
            self.item_elements.append(item_element)
            self.add_renderable(item_element)

            # # Update inventory
            # for i, elem in enumerate(self.item_elements):
            #     elem.set_new_address((game.party.inventory, i))

    def update(self, game, system):
        self.shard_element.set_text(str(game.party.shards))