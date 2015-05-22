import pygame
from pygame import display

_screen = None

_resolution = (800, 600)
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
        obj.draw(_screen)
        
    display.flip()



class Renderable(object):
    renderables = []

    def __init__(self, pos):
        self.pos = pos
        Renderable.renderables.append(self)

    def delete(self):
        Renderable.renderables.remove(self)

    def draw(self, surface):
        pass
