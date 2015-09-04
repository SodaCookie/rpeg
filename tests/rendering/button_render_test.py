import pygame

from engine.rendering.element.button import Button

class MockGameObject:
    mouse_x = 0
    mouse_y = 0
    mouse_button = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
button = Button("Hello World", 20, 100, 100, None, True)
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
    button.render(screen, m)
    clock.tick(60)

pygame.quit()