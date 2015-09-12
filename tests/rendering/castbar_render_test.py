import pygame

from engine.game.player.player import Player
from engine.ui.manager.castbar_manager import CastBarManager
from engine.game.move.built_moves import *

class MockGameObject:
    mouse_x = 0
    mouse_y = 0
    mouse_button = (0, 0, 0)
    selected_player = None

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
p = Player("Player")
p.castbar[0] = slash
p.castbar[3] = magic_bolt
p.castbar[9] = magic_blast
m = MockGameObject()
m.selected_player = p
cbm = CastBarManager(300)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if m.selected_player:
                m.selected_player = None
            else:
                m.selected_player = p
    pygame.display.flip()
    m.mouse_x, m.mouse_y = pygame.mouse.get_pos()
    m.mouse_button = pygame.mouse.get_pressed()
    screen.fill((0, 0, 0))
    cbm.update(m)
    cbm.render(screen, m)
    clock.tick(60)

pygame.quit()