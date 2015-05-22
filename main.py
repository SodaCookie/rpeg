import pygame
from pygame import time, event

import view
import controller
import main_menu

from objects import effect
from objects import monster
from objects import player
from objects import item
from objects import moves

if __name__ == "__main__":

    view.init_pygame()

    main_menu.open()

    running = True
    while running:
        event.pump()    # le hideous break condition
        if event.peek(pygame.QUIT):
            running = False

        controller.update()

        view.render()
        time.wait(30)

    view.quit()
