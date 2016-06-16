import math
import sys
import random

import pygame

# Used to draw seeded frames
_random_seed = random.randint(0, sys.maxsize)

def draw_highlight_frame(width, height, highlight, scale=4, borderwidth=1,
        seed=None):
    """draws a highlighted frame with a given colour"""
    scale = 4
    frame = draw_frame(width, height, scale, borderwidth, seed)
    frame.fill(highlight, (0, 0, scale, frame.get_height()))
    frame.fill(highlight, (0, 0, frame.get_width(), scale))
    frame.fill(highlight,
        (frame.get_width() - scale, 0, scale, frame.get_height()))
    frame.fill(highlight,
        (0, frame.get_height() - scale, frame.get_width(), scale))
    frame.fill((0, 0, 0, 0), (0, 0, scale * 2, scale * 2))
    frame.fill((0, 0, 0, 0),
        (0, frame.get_height() - scale * 2, scale * 2, scale * 2))
    frame.fill((0, 0, 0, 0),
        (frame.get_width() - scale * 2, 0, scale * 2, scale * 2))
    frame.fill((0, 0, 0, 0),
        ((frame.get_width() - scale * 2,frame.get_height() - scale * 2),
         (scale * 2, scale * 2)))
    frame.fill(highlight, (scale, scale, scale, scale))
    frame.fill(highlight,
        (scale, frame.get_height() - scale * 2, scale, scale))
    frame.fill(highlight,
        (frame.get_width() - scale * 2, scale, scale, scale))
    frame.fill(highlight,
        ((frame.get_width() - scale * 2, frame.get_height() - scale * 2),
         (scale, scale)))
    return frame

def draw_frame(width, height, scale=4, borderwidth=1, seed=None):
    """Method for drawing a frame surface."""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))

    texture = pygame.image.load("image/ui/texture.png").convert()
    texture = pygame.transform.scale(texture,
        (texture.get_width() * scale, texture.get_height() * scale))
    border = pygame.image.load("image/ui/border.png").convert()
    border = pygame.transform.scale(border,
        (border.get_width() * scale, border.get_height() * scale))
    border_vertical = pygame.transform.rotate(border, 90)

    texture_w = int(math.ceil(width / scale)) + 1
    texture_h = int(math.ceil(height / scale)) +1

    if seed is None:
        seed = random.randint(0, texture.get_width() // scale)
    start_x = -(seed * _random_seed % texture.get_width())
    start_y = -(seed * _random_seed % texture.get_height())

    # fill in texture
    for i in range(texture_w):
        for j in range(texture_h):
            surface.blit(texture,
                (start_x + borderwidth + i * texture.get_width(),
                 start_y + borderwidth + j * texture.get_height()))

    # add borders
    for i in range(texture_w):
        surface.blit(border, (i * border.get_width(), 0))
        surface.blit(border, (i * border.get_width(),
            height - scale * borderwidth))
    for i in range(texture_h):
        surface.blit(border_vertical,
            (0, i * border_vertical.get_height()))
        surface.blit(border_vertical, (width - scale * borderwidth,
            i * border_vertical.get_height()))

    # fix corners
    surface.fill((0, 0, 0, 0),
        (0, 0, scale * borderwidth * 2, scale * borderwidth * 2))
    surface.fill((0, 0, 0, 0),
        (0, height - scale * borderwidth * 2,
         scale * borderwidth * 2, scale * borderwidth * 2))
    surface.fill((0, 0, 0, 0),
        (width - scale * borderwidth * 2, height - scale * borderwidth * 2,
         scale * borderwidth * 2, scale * borderwidth * 2))
    surface.fill((0, 0, 0, 0),
        (width - scale * borderwidth * 2, 0,
         scale * borderwidth * 2, scale * borderwidth * 2))

    # fill corner
    # stop gauge measure until maybe i decide to use real corners...
    surface.blit(border, (scale, scale),
        (0, 0, scale, scale))
    surface.blit(border, (scale, height - scale * borderwidth * 2),
        (0, 0, scale, scale))
    surface.blit(border, (width - scale * borderwidth * 2,
        height - scale * borderwidth * 2), (0, 0, scale, scale))
    surface.blit(border, (width - scale * borderwidth * 2, scale),
        (0, 0, scale, scale))

    return surface