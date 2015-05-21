import pygame
from pygame import time, event

import view
import controller
from text import Text
from button import Button

import effects
import monster
import player
import item
import moves


if __name__ == "__main__":

    view.init_pygame()

    running = True
    while running:
        event.pump()
        if event.peek(pygame.QUIT):
            running = False

        controller.update()
        view.render()
        time.wait(30)

    view.quit()
