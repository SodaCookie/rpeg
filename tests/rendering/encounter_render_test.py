import pygame

from engine.game.monster.monster import Monster
from engine.ui.manager.encounter_manager import EncounterManager

class MockGameObject:
    mouse_x = 0
    mouse_y = 0
    mouse_button = (0, 0, 0)
    encounter = []

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
m = MockGameObject()
m.encounter = [Monster() for i in range(3)]
encounter = EncounterManager()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    m.mouse_x, m.mouse_y = pygame.mouse.get_pos()
    m.mouse_button = pygame.mouse.get_pressed()
    screen.fill((0, 0, 0))
    encounter.update(m)
    encounter.render(screen, m)
    clock.tick(60)

pygame.quit()