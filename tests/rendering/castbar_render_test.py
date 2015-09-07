import pygame

from engine.ui.manager.castbar_manager import CastBarManager

class MockGameObject:
    mouse_x = 0
    mouse_y = 0
    mouse_button = (0, 0, 0)
    selected_player = None

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
m = MockGameObject()
cbm = CastBarManager(300)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    m.mouse_x, m.mouse_y = pygame.mouse.get_pos()
    m.mouse_button = pygame.mouse.get_pressed()
    screen.fill((0, 0, 0))
    cbm.update(m)
    cbm.render(screen, m)
    clock.tick(60)

pygame.quit()