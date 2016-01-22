"""Defines the LevelUpManager"""
from functools import partial

import pygame

from engine.ui.core.manager import Manager
from engine.ui.core.zone import Zone
import engine.ui.element as element

class LevelUpManager(Manager):
    """LevelUpManager is used to render the player level up screen
    and bind calls to player level up"""

    class MoveRenderManager(Manager):
        """Handles the rendering of a single move in the level up manager"""

        def __init__(self, width, height, x, y):
            super().__init__()
            self.move = None
            self.confirm_move = False # Makes sure player is absolutely sure
            self.hover = False
            self.width = width
            self.height = height
            self.x = x
            self.y = y
            self.neutral_image = None
            self.hover_image = None

        def set_hover(self, hover):
            self.hover = hover

        def update_move(self, move):
            # Clear renderables
            self.renderables = []
            # Set Move
            self.move = move

            # Create window element and save hover and neutral images
            self.window_element = element.Window(self.width, self.height,
                self.x, self.y)
            self.neutral_image = self.window_element.surface
            self.hover_image = element.Window.draw(self.width, self.height,
                                                   (255, 255, 0))
            self.renderables.append(self.window_element)

            # Draw the move image
            icon_filename = move.icon
            if icon_filename:
                icon_surface = pygame.image.load(icon_filename).convert()
            else:
                icon_surface = \
                    pygame.image.load(element.Slot.DEFAULTICON).convert()
            icon_surface = pygame.transform.scale(icon_surface,
                (icon_surface.get_width()*6, icon_surface.get_height()*6))
            icon_element = element.Image(icon_surface,
                self.x+self.width//2-icon_surface.get_width()//2, self.y+5)
            self.renderables.append(icon_element)

            # Text elements
            name_element = element.Text(move.name.title(), 40, self.x,
                self.y+100, width=self.width, justify=element.Text.CENTER)
            description_element = element.Text(move.description, 20, self.x,
                self.y+130, width=self.width, justify=element.Text.CENTER)
            self.renderables.append(name_element)
            self.renderables.append(description_element)

        def update(self, game):
            super().update(game)

        def render(self, surface, game):
            if self.hover:
                self.window_element.surface = self.hover_image
            else:
                self.window_element.surface = self.neutral_image
            super().render(surface, game)


    def __init__(self, screen_width, screen_height):
        super().__init__()
        # Class attributes
        self.level_up_moves = None
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Create dark screen
        screen_image = pygame.Surface((screen_width, screen_height),
                                      pygame.SRCALPHA)
        screen_image.fill((0, 0, 0, 100))
        screen_element = element.Image(screen_image, 0, 0)
        self.renderables.append(screen_element)

        # Create move rendering managers
        self.managers = []

    def update_moves(self, player):
        """Updates the move managers"""
        self.managers = []
        self.zones = []
        PADDING = 50
        width = self.screen_width // 3 - PADDING * 2
        for i, move in enumerate(player.level_up_moves):
            manager = self.MoveRenderManager(width, width,
                self.screen_width // 3 * i + PADDING,
                self.screen_height // 2 - width // 2)
            manager.update_move(move)
            self.managers.append(manager)

            # Create partials
            on_click = partial(self.on_move_on_click, manager)
            off_click = partial(self.on_move_off_click, manager)
            on_hover = partial(self.on_move_on_hover, manager)
            off_hover = partial(self.on_move_off_hover, manager)

            # Create Zone
            manager_zone = Zone((
                self.screen_width // 3 * i + PADDING,
                self.screen_height // 2 - width // 2,
                width, width),
                on_click=on_click,
                off_click=off_click,
                on_hover=on_hover,
                off_hover=off_hover)
            self.zones.append(manager_zone)

    def update(self, game):
        if game.focus_window == "level":
            if game.selected_player.level_up_moves != self.level_up_moves:
                if game.selected_player.level_up_moves:
                    self.update_moves(game.selected_player)
                    self.level_up_moves = game.selected_player.level_up_moves
            super().update(game)
            for manager in self.managers:
                manager.update(game)

    def render(self, surface, game):
        if game.focus_window == "level":
            super().render(surface, game)
            for manager in self.managers:
                manager.render(surface, game)

    @staticmethod
    def on_move_on_click(manager, game):
        manager.set_hover(False)
        manager.confirm_move = True

    @staticmethod
    def on_move_off_click(manager, game):
        manager.set_hover(True)
        if manager.confirm_move:
            game.selected_player.level_up(manager.move)
            game.focus_window = None

    @staticmethod
    def on_move_on_hover(manager, game):
        manager.set_hover(True)

    @staticmethod
    def on_move_off_hover(manager, game):
        manager.set_hover(False)
        manager.confirm_move = False
