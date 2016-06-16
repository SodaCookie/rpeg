import random
import pygame

from engine.system import Message

from engine.ui.element.abstractbutton import AbstractButton
from engine.ui.element.itemslot import ItemSlot
import engine.ui.draw.frame as frame
import engine.ui.draw.simple as simple

class MoveCard(AbstractButton):
    """Handles the rendering of a single move in the level up manager"""

    def __init__(self, name, x, y, width, height):
        super().__init__(name, (x, y, width, height))
        self.title_font = pygame.font.Font("assets/fonts/VT323-Regular.ttf",
            40)
        self.font = pygame.font.Font("assets/fonts/VT323-Regular.ttf", 20)
        self.move = None
        self.width = width
        self.height = height
        self.draw_seed = random.randint(0, 99)

    def on_hovered(self, game, system):
        system.message("sound", Message("ui",
                "data/sound/menu_select_sfx.wav"))

    def render_neutral(self, game):
        surface = frame.draw_frame(self.width, self.height,
            seed=self.draw_seed)
        if self.move is None:
            return surface

        # Draw the move self.image
        icon_filename = self.move.icon
        if icon_filename:
            icon_surface = simple.draw_image(icon_filename, 6)
        else:
            icon_surface = simple.draw_image(ItemSlot.DEFAULTICON, 6)

        surface.blit(icon_surface,
            (self.width // 2 - icon_surface.get_width() // 2, 12))

        # Text elements
        surface.blit(simple.draw_text(self.move.name.title(), self.title_font,
            (255, 255, 255), self.width - 24, justify="center"), (12, 100))
        surface.blit(simple.draw_text(self.move.description, self.font,
            (255, 255, 255), self.width - 24, justify="center"), (12, 130))
        return surface

    def render_hover(self, game):
        surface = frame.draw_highlight_frame(self.width, self.height,
            highlight=(255, 255, 0), seed=self.draw_seed)
        if self.move is None:
            return surface

        # Draw the move image
        icon_filename = self.move.icon
        if icon_filename:
            icon_surface = simple.draw_image(icon_filename, 6)
        else:
            icon_surface = simple.draw_image(ItemSlot.DEFAULTICON, 6)

        surface.blit(icon_surface,
            (self.width // 2 - icon_surface.get_width() // 2, 12))

        # Text elements
        surface.blit(simple.draw_text(self.move.name.title(), self.title_font,
            (255, 255, 0), self.width - 24, justify="center"), (12, 100))
        surface.blit(simple.draw_text(self.move.description, self.font,
            (255, 255, 0), self.width - 24, justify="center"), (12, 130))
        return surface

    def render_clicked(self, game):
        surface = frame.draw_highlight_frame(self.width, self.height,
            highlight=(0, 255, 0), seed=self.draw_seed)
        if self.move is None:
            return surface

        # Draw the move iself.mage
        icon_filename = self.move.icon
        if icon_filename:
            icon_surface = simple.draw_image(icon_filename, 6)
        else:
            icon_surface = simple.draw_image(ItemSlot.DEFAULTICON, 6)

        surface.blit(icon_surface,
            (self.width // 2 - icon_surface.get_width() // 2, 12))

        # Text elements
        surface.blit(simple.draw_text(self.move.name.title(), self.title_font,
            (0, 255, 0), self.width - 24, justify="center"), (12, 100))
        surface.blit(simple.draw_text(self.move.description, self.font,
            (0, 255, 0), self.width - 24, justify="center"), (12, 130))
        return surface

    def on_click(self, game, system):
        system.message("game", Message("level-player", self.move))
        system.message("ui", Message("pop-bg", self.move))
        system.message("ui", Message("layout", "character"))
        system.message("ui", Message("refresh-character"))

    def update_move(self, move):
        # Set Move
        self.move = move
        self.set_dirty(True)
