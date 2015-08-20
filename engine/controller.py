import pygame
from pygame import event

BATTLESTART = pygame.USEREVENT
BATTLETICK = pygame.USEREVENT + 1
BATTLEEND = pygame.USEREVENT + 2

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

    if event.get(BATTLESTART):
        BattleController._start_battle()

    if event.get(BATTLETICK):
        BattleController._handle_battle()

    if event.get(BATTLEEND):
        BattleController._end_battle()


class BattleController(object):
    battle_controllers = []
    delta_time = pygame.time.get_ticks()

    @staticmethod
    def _handle_battle():
        delta = pygame.time.get_ticks() - BattleController.delta_time
        for controller in BattleController.battle_controllers:
            controller.handle_battle(delta/1000)
        BattleController.delta_time = pygame.time.get_ticks()

    @staticmethod
    def _start_battle():
        BattleController.delta_time = pygame.time.get_ticks()
        for controller in BattleController.battle_controllers:
            controller.handle_start_battle()

    @staticmethod
    def _end_battle():
        for controller in BattleController.battle_controllers:
            controller.handle_end_battle()

    def __init__(self):
        BattleController.battle_controllers.append(self)

    def delete(self):
        BattleController.battle_controllers.remove(self)

    def handle_battle(self, delta): # in seconds
        pass

    def handle_start_battle(self):
        pass

    def handle_end_battle(self):
        pass


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
