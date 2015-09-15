# import pygame

# from engine.ui.core.renderable import Renderable
# from engine.ui.core.zone import Zone
# from engine.ui.core.bindable import Bindable
# from engine.ui.element.window import Window
# from engine.ui.element.text import Text

# class MouseHoverManager(Renderable, Bindable):

#     # Can expand to add more elements like images as well to create specific tooltips
#     # I could probably clean this up? Maybe just have window and text attributes >.<
#     def __init__(self, window_width, window_height, text, size, colour=pygame.Color("white"), text_width=None, justify="left"):
#         super().__init__()
#         self.text = text
#         self.colour = colour
#         self.size = size
#         self.text_width = text_width
#         self.justify = justify
#         self.window_width = window_width
#         self.window_height = window_height
#         self.x_offset = 0
#         self.y_offset = 0
#         self.surface = self.draw(self.window_width, self.window_height, None, self.text, self.size, self.colour, self. text_width, self.justify)

#     def draw(self, width, height, highlight, text, size, colour, text_width, justify):
#         window = Window.draw(width, height, highlight)
#         text = Text.draw(text, size, colour, text_width, justify)
#         surface = window.blit(window, (0, 0))
#         return surface

#     def render(self, surface, game):
#         if self.bound.state == Zone.HOVERED:
#             super().render(surface, game)

import engine.game as Game
from engine.ui.core.manager import Manager
import engine.ui.core.zone as Zone

class MouseHoverManager(Manager):
    """Handles surfaces that should be drawn when mouse is
    hovered over specific zones"""

    def __init__(self):
        super().__init__()

    def render(self, surface, game):
        if game.current_hover:
            surface.blit(game.current_hover, (game.mouse_x + game.hover_x, game.hover_y + game.mouse_y))