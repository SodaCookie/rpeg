"""Defines the CastbarManager"""
import pygame

from engine.ui.core.manager import Manager
import engine.ui.element as element

class CastBarManager(Manager):

    def __init__(self, y):
        super().__init__()
        SCALE = 4
        window_width = 566
        window_x = pygame.display.get_surface().get_width()//2-window_width//2-SCALE
        self.renderables.append(element.Window(window_width, 60, window_x, y))
        for i in range(1, 11):
            self.renderables.append(element.MoveIcon(None, 8+window_x+(i-1)*56, y+7))
            self.renderables.append(element.Text(str(i)[-1], 16, 50+window_x+(i-1)*56, y+40))