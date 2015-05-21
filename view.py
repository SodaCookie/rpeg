import pygame
from pygame import display

_screen = None
_resolution = (800,600)

def init_pygame():
    global _screen, _resolution

    pygame.init()
    _screen = display.set_mode(_resolution)



def quit():
    display.quit()
    pygame.quit()



def render():
    global _screen

    _screen.fill((255, 255, 255))
    for obj in Renderable.renderables:
        obj.draw(_screen)
        
    display.flip()



class Renderable(object):
    renderables = []

    def __init__(self, pos):
        self.pos = pos
        Renderable.renderables.append(self)

    def __del__(self):
        Renderable.renderables.remove(self)

    def draw(self, surface):
        pass

