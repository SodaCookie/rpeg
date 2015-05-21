import pygame
from pygame import time, event

import view
import controller
import main_menu

import effects
import monster
import player
import item
import moves

if __name__ == "__main__":

    view.init_pygame()

    main_menu.open(None, None)

    running = True
    while running:
        event.pump()    # le hideous break condition
        if event.peek(pygame.QUIT):
            running = False

        controller.update()

        view.render()
        time.wait(30)

    main_menu.close()

    view.quit()
