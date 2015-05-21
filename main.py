import pygame
from pygame import time, event

import view
import controller
from text import Text, TextInfo
from button import Button, ButtonInfo

import effects
import monster
import player
import item
import moves


if __name__ == "__main__":

    view.init_pygame()

    top_kek = Text((400,300), TextInfo(fontsize=50), "TOP KEK")

    running = True
    while running:
        event.pump()    # le hideous break condition
        if event.peek(pygame.QUIT):
            running = False

        controller.update()
        view.render()
        time.wait(30)

    view.quit()
