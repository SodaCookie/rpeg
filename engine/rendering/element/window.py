import pygame
import random
import math

from engine.rendering.core.renderable import Renderable

class Window(Renderable):
    """docstring for Window"""

    def __init__(self, width, height, x, y):
        super(Window, self).__init__()
        self.width = width
        self.height = height
        self.surface = None
        self.x = x
        self.y = y
        self.draw()

    def draw(self):
        """method for drawing the actual surface."""
        SCALE = 4 # temporary until we figure out where scale will go
        BORDERWIDTH = 1

        self.surface = pygame.Surface(
            (self.width+BORDERWIDTH*SCALE*2, self.height+BORDERWIDTH*SCALE*2),
             pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))

        texture = pygame.image.load("image/ui/texture.png").convert()
        texture = pygame.transform.scale(texture,
            (texture.get_width()*SCALE, texture.get_height()*SCALE))
        border = pygame.image.load("image/ui/border.png").convert()
        border = pygame.transform.scale(border,
            (border.get_width()*SCALE, border.get_height()*SCALE))
        border_vertical = pygame.transform.rotate(border, 90)

        texture_w = int(math.ceil(self.width/SCALE))+1
        texture_h = int(math.ceil(self.height/SCALE))+1

        start_x = random.randint(-texture.get_width()//SCALE, 0)
        start_y = random.randint(-texture.get_height()//SCALE, 0)

        # fill in texture
        for i in range(texture_w):
            for j in range(texture_h):
                self.surface.blit(texture,
                    (start_x+BORDERWIDTH+i*texture.get_width(),
                     start_y+BORDERWIDTH+j*texture.get_height()))

        # add borders
        for i in range(texture_w):
            self.surface.blit(border, (i*border.get_width(), 0))
            self.surface.blit(border, (i*border.get_width(),
                self.height+SCALE*BORDERWIDTH))
        print(texture_w, texture_h)
        for i in range(texture_h):
            self.surface.blit(border_vertical,
                (0, i*border_vertical.get_height()))
            self.surface.blit(border_vertical, (self.width+SCALE*BORDERWIDTH,
                i*border_vertical.get_height()))

        # remove corners
        self.surface.fill((0, 0, 0, 0),
            (0, 0, SCALE*BORDERWIDTH, SCALE*BORDERWIDTH))
        self.surface.fill((0, 0, 0, 0),
            (0, self.height+SCALE*BORDERWIDTH,
             SCALE*BORDERWIDTH, SCALE*BORDERWIDTH))
        self.surface.fill((0, 0, 0, 0),
            (self.width+SCALE*BORDERWIDTH, self.height+SCALE*BORDERWIDTH,
             SCALE*BORDERWIDTH, SCALE*BORDERWIDTH))
        self.surface.fill((0, 0, 0, 0),
            (self.width+SCALE*BORDERWIDTH, 0,
             SCALE*BORDERWIDTH, SCALE*BORDERWIDTH))

    def render(self, surface, game):
        SCALE = 4
        BORDERWIDTH = 1
        tmp_surface = self.surface.copy()
        draw_surface = tmp_surface.subsurface(
            (BORDERWIDTH*SCALE, BORDERWIDTH*SCALE,
             self.width-BORDERWIDTH*SCALE*2, self.height-BORDERWIDTH*SCALE*2))
        surface.blit(self.surface, (self.x, self.y))

