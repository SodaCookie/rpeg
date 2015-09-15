import pygame

import engine.ui.manager.mouse_hover_manager as MouseHoverManager

class MockGameObject:
    mouse_x = 0
    mouse_y = 0
    mouse_button = (0, 0, 0)

    hover_x = 20
    hover_y = -20
    current_hover = pygame.image.load("image\monster\slime1_base.png")

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

mh = MouseHoverManager.MouseHoverManager()
m = MockGameObject()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    m.mouse_x, m.mouse_y = pygame.mouse.get_pos()
    m.mouse_button = pygame.mouse.get_pressed()
    screen.fill((0, 0, 0))
    mh.render(screen, m)
    clock.tick(60)

pygame.quit()