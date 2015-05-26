import pygame
from pygame import event

def update():
    if event.peek(pygame.MOUSEMOTION):
        for e in event.get(pygame.MOUSEMOTION):
            MouseController.handle_mouse_motion(e)

    if event.peek(pygame.MOUSEBUTTONDOWN):
        for e in event.get(pygame.MOUSEBUTTONDOWN):
            MouseController.handle_mouse_button_down(e)

    if event.peek(pygame.MOUSEBUTTONUP):
        for e in event.get(pygame.MOUSEBUTTONUP):
            MouseController.handle_mouse_button_up(e)

    if event.peek(pygame.USEREVENT):
        pass

def merge(*funcs):
    for func in funcs:
        func()

class MouseController(object):
    mouse_controllers = []

    @staticmethod
    def handle_mouse_motion(e):
        for controller in MouseController.mouse_controllers:
            controller.mouse_motion(e.buttons, e.pos, e.rel)

    @staticmethod
    def handle_mouse_button_down(e):
        for controller in MouseController.mouse_controllers:
            controller.mouse_button_down(e.button, e.pos)

    @staticmethod
    def handle_mouse_button_up(e):
        for controller in MouseController.mouse_controllers:
            controller.mouse_button_up(e.button, e.pos)

    def __init__(self):
        MouseController.mouse_controllers.append(self)

    def delete(self):
        MouseController.mouse_controllers.remove(self)

    def mouse_motion(self, buttons, pos, rel):
        pass

    def mouse_button_down(self, button, pos):
        pass

    def mouse_button_up(self, button, pos):
        pass

if __name__ == "__main__":
    pass
