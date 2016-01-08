import random

import pygame

from engine.ui.manager.travel_manager import TravelManager
from engine.game.dungeon.dungeon import Dungeon

class MockGameObject:
    mouse_x = 0
    mouse_y = 0
    mouse_button = (0, 0, 0)
    current_location = None
    current_dungeon = None

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
d = Dungeon("catacomb", "normal")
m = MockGameObject()
m.current_dungeon = d
m.current_location = d.start
travel_manager = TravelManager(800, 300, 100, 100)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
    pygame.display.flip()
    m.mouse_x, m.mouse_y = pygame.mouse.get_pos()
    m.mouse_button = pygame.mouse.get_pressed()
    screen.fill((0, 0, 0))
    travel_manager.update(m)
    travel_manager.render(screen, m)
    clock.tick(60)

pygame.quit()