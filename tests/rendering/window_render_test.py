import pygame

from engine.rendering.element.window import Window

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

window = Window(500, 400, 100, 100)
border = pygame.image.load("image/ui/border.png").convert()
border = pygame.transform.scale(border,
    (border.get_width()*4, border.get_height()*4))
border_vertical = pygame.transform.rotate(border, 90)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    screen.fill((0, 0, 0))
    window.render(screen, None)
    screen.blit(border_vertical, (0, 0))
    clock.tick(60)

pygame.quit()