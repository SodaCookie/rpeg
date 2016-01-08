import pygame

from engine.game.player.player import Player
from engine.ui.manager.party_manager import PartyManager

class MockGameObject:
    mouse_x = 0
    mouse_y = 0
    mouse_button = (0, 0, 0)
    party = []

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
m = MockGameObject()
m.party = [Player("Player") for i in range(3)]
pm = PartyManager()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    m.mouse_x, m.mouse_y = pygame.mouse.get_pos()
    m.mouse_button = pygame.mouse.get_pressed()
    screen.fill((0, 0, 0))
    pm.update(m)
    pm.render(screen, m)
    clock.tick(60)

pygame.quit()