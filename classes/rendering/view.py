import pygame
import logging
from pygame import display

_screen = None

SCALE = 4

_resolution = (1280, 720)
def set_resolution(new_resolution):
    global _resolution
    _resolution = new_resolution
    screen = display.set_mode(_resolution)
def get_resolution():
    global _resolution
    return _resolution

def init_pygame():
    global _screen, _resolution

    pygame.init()
    _screen = display.set_mode(_resolution)



def quit():
    display.quit()
    pygame.quit()



def render():
    global _screen

    _screen.fill((0, 0, 0))
    for obj in Renderable.renderables:
        if obj.visible:
            obj.draw(_screen)

    display.flip()



class Renderable(object):
    renderables = []

    def __init__(self, pos):
        self.pos = pos
        self.visible = False

    def display(self):
        self.visible = True
        if self not in Renderable.renderables:
            Renderable.renderables.append(self)

    def delete(self):
        """Will attempt to delete """
        if self in Renderable.renderables:
            Renderable.renderables.remove(self)
        else:
            logging.info("Attempted to delete already non-displayed renderable: %s"%str(self))

    def hide(self):
        self.visible = False

    def move(self, pos):
        self.pos = pos

    def draw(self, surface):
        pass
