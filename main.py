import pygame
from pygame import time, event

import view
import controller
import main_menu

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
