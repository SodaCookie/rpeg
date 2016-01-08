import pygame
import random
import math

from engine.ui.core.renderable import Renderable

class Window(Renderable):
    """docstring for Window"""

    def __init__(self, width, height, x, y, highlight=None):
        super(Window, self).__init__()
        self.width = width
        self.height = height
        self.surface = self.draw(self.width, self.height, highlight)
        self.x = x
        self.y = y

    @classmethod
    def highlight_window(self, window, highlight):
        SCALE = 4
        window = window.copy()
        window.fill(highlight, (0, 0, SCALE, window.get_height()))
        window.fill(highlight, (0, 0, window.get_width(), SCALE))
        window.fill(highlight,
            (window.get_width()-SCALE, 0, SCALE, window.get_height()))
        window.fill(highlight,
            (0, window.get_height()-SCALE, window.get_width(), SCALE))
        window.fill((0, 0, 0, 0), (0, 0, SCALE*2, SCALE*2))
        window.fill((0, 0, 0, 0),
            (0, window.get_height()-SCALE*2, SCALE*2, SCALE*2))
        window.fill((0, 0, 0, 0),
            (window.get_width()-SCALE*2, 0, SCALE*2, SCALE*2))
        window.fill((0, 0, 0, 0),
            (window.get_width()-SCALE*2, window.get_height()-SCALE*2, SCALE*2, SCALE*2))
        window.fill(highlight, (SCALE, SCALE, SCALE, SCALE))
        window.fill(highlight,
            (SCALE, window.get_height()-SCALE*2, SCALE, SCALE))
        window.fill(highlight,
            (window.get_width()-SCALE*2, SCALE, SCALE, SCALE))
        window.fill(highlight,
            (window.get_width()-SCALE*2, window.get_height()-SCALE*2, SCALE, SCALE))
        return window

    @classmethod
    def draw(self, width, height, highlight):
        """method for drawing the actual surface."""
        SCALE = 4 # temporary until we figure out where scale will go
        BORDERWIDTH = 1

        surface = pygame.Surface(
            (width+BORDERWIDTH*SCALE*2, height+BORDERWIDTH*SCALE*2),
             pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        texture = pygame.image.load("image/ui/texture.png").convert()
        texture = pygame.transform.scale(texture,
            (texture.get_width()*SCALE, texture.get_height()*SCALE))
        border = pygame.image.load("image/ui/border.png").convert()
        border = pygame.transform.scale(border,
            (border.get_width()*SCALE, border.get_height()*SCALE))
        border_vertical = pygame.transform.rotate(border, 90)

        texture_w = int(math.ceil(width/SCALE))+1
        texture_h = int(math.ceil(height/SCALE))+1

        start_x = random.randint(-texture.get_width()//SCALE, 0)
        start_y = random.randint(-texture.get_height()//SCALE, 0)

        # fill in texture
        for i in range(texture_w):
            for j in range(texture_h):
                surface.blit(texture,
                    (start_x+BORDERWIDTH+i*texture.get_width(),
                     start_y+BORDERWIDTH+j*texture.get_height()))

        # add borders
        for i in range(texture_w):
            surface.blit(border, (i*border.get_width(), 0))
            surface.blit(border, (i*border.get_width(),
                height+SCALE*BORDERWIDTH))
        for i in range(texture_h):
            surface.blit(border_vertical,
                (0, i*border_vertical.get_height()))
            surface.blit(border_vertical, (width+SCALE*BORDERWIDTH,
                i*border_vertical.get_height()))

        # fix corners
        surface.fill((0, 0, 0, 0),
            (0, 0, SCALE*BORDERWIDTH*2, SCALE*BORDERWIDTH*2))
        surface.fill((0, 0, 0, 0),
            (0, height,
             SCALE*BORDERWIDTH*2, SCALE*BORDERWIDTH*2))
        surface.fill((0, 0, 0, 0),
            (width, height,
             SCALE*BORDERWIDTH*2, SCALE*BORDERWIDTH*2))
        surface.fill((0, 0, 0, 0),
            (width, 0,
             SCALE*BORDERWIDTH*2, SCALE*BORDERWIDTH*2))

        # fill corner
        # stop gauge measure until maybe i decide to use real corners...
        surface.blit(border, (SCALE, SCALE),
            (0, 0, SCALE, SCALE))
        surface.blit(border, (SCALE, height),
            (0, 0, SCALE, SCALE))
        surface.blit(border, (width, height),
            (0, 0, SCALE, SCALE))
        surface.blit(border, (width, SCALE),
            (0, 0, SCALE, SCALE))

        if highlight:
            return self.highlight_window(surface, highlight)

        return surface

    def render(self, surface, game):
        surface.blit(self.surface, (self.x, self.y))

