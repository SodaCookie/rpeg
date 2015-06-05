import pygame
from pygame import time, event

import classes.rendering.view as view
import classes.controller as controller
from classes.main_menu import MainMenu
from classes.game_menu import GameMenu

# So we can just define all our transitions like this...
# This kinda makes menus singletons anyways. Ideally we have
# some sort of menu stack and transitions are attached to
# events which are triggered by buttons.
def singleplayer():
    global _main_menu, _game_menu
    _main_menu.delete()
    _main_menu = None
    _game_menu = GameMenu()

if __name__ == "__main__":

    view.init_pygame()

    _main_menu = MainMenu(singleplayer)
    _main_menu.display()

    running = True
    while running:
        event.pump()    # le hideous break condition
        if event.peek(pygame.QUIT):
            running = False

        controller.update()

        view.render()
        time.wait(30)

    view.quit()
