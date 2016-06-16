"""Defines the LevelUpManager"""
import pygame

from engine.ui.core.manager import Manager
import engine.ui.element as element

class LevelUpManager(Manager):
    """LevelUpManager is used to render the player level up screen
    and bind calls to player level up"""

    def __init__(self):
        super().__init__("level", 0, 0)

        # Elements
        width, height = pygame.display.get_surface().get_size()
        self.move_elements = []
        for i in range(3):
            move = element.MoveCard("move-%d" % i, width // 4 * (i + 1) - 150,
                height // 2 - 150, 300, 300)
            self.add_renderable(move)
            self.move_elements.append(move)

    def load_moves(self, moves):
        for move, elem in zip(moves, self.move_elements):
            elem.update_move(move)

    #     # Create dark screen
    #     screen_image = pygame.Surface((screen_width, screen_height),
    #                                   pygame.SRCALPHA)
    #     screen_image.fill((0, 0, 0, 100))
    #     screen_element = element.Image(screen_image, 0, 0)
    #     self.renderables.append(screen_element)

    #     # Create move rendering managers
    #     self.managers = []

    # def update_moves(self, player):
    #     """Updates the move managers"""
    #     self.managers = []
    #     self.zones = []
    #     PADDING = 50
    #     width = self.screen_width // 3 - PADDING * 2
    #     for i, move in enumerate(player.level_up_moves):
    #         manager = self.MoveRenderManager(width, width,
    #             self.screen_width // 3 * i + PADDING,
    #             self.screen_height // 2 - width // 2)
    #         manager.update_move(move)
    #         self.managers.append(manager)

    #         # Create partials
    #         on_click = partial(self.on_move_on_click, manager)
    #         off_click = partial(self.on_move_off_click, manager)
    #         on_hover = partial(self.on_move_on_hover, manager)
    #         off_hover = partial(self.on_move_off_hover, manager)

    #         # Create Zone
    #         manager_zone = Zone((
    #             self.screen_width // 3 * i + PADDING,
    #             self.screen_height // 2 - width // 2,
    #             width, width),
    #             on_click=on_click,
    #             off_click=off_click,
    #             on_hover=on_hover,
    #             off_hover=off_hover)
    #         self.zones.append(manager_zone)

    # def update(self, game):
    #     if game.focus_window == "level":
    #         if game.selected_player.level_up_moves != self.level_up_moves:
    #             if game.selected_player.level_up_moves:
    #                 self.update_moves(game.selected_player)
    #                 self.level_up_moves = game.selected_player.level_up_moves
    #         super().update(game)
    #         for manager in self.managers:
    #             manager.update(game)

    # def render(self, surface, game):
    #     if game.focus_window == "level":
    #         super().render(surface, game)
    #         for manager in self.managers:
    #             manager.render(surface, game)

    # @staticmethod
    # def on_move_on_click(manager, game):
    #     manager.set_hover(False)
    #     manager.confirm_move = True

    # @staticmethod
    # def on_move_off_click(manager, game):
    #     manager.set_hover(True)
    #     if manager.confirm_move:
    #         game.selected_player.level_up(manager.move)
    #         game.focus_window = None

    # @staticmethod
    # def on_move_on_hover(manager, game):
    #     manager.set_hover(True)

    # @staticmethod
    # def on_move_off_hover(manager, game):
    #     manager.set_hover(False)
    #     manager.confirm_move = False
