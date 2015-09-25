import pygame

from engine.ui.manager.mouse_hover_manager import MouseHoverManager
from engine.ui.element.slot import Slot

from engine.game.item.item import Item
from engine.game.move.move import Move

class MockGame():
    # selected_player = None
    # selected_move = None
    mouse_x = 0
    mouse_y = 0
    mouse_button = (0, 0, 0)
    party = []

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

mock = MockGame()
mhm = MouseHoverManager()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    mock.mouse_x, mock.mouse_y = pygame.mouse.get_pos()
    mock.mouse_button = pygame.mouse.get_pressed()
    mhm.update()
    # pm.update(mock)
    # ccm.update(mock)
    screen.fill((0, 0, 0))
    # pm.render(screen, mock)
    # ccm.render(screen, mock)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()