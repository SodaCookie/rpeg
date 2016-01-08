import pygame

from engine.ui.element.button import Button
from engine.ui.core.zone import Zone

class MockGameObject:
    mouse_x = 0
    mouse_y = 0
    mouse_button = (0, 0, 0)

def hello_world(game):
    print("Hello World!")

def spooky(game):
    print("Spooky!")

def ghosts(game):
    print("Ghosts!")

def lift(game):
    print("Lift")

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
button = Button("Hello World", 20, 100, 100)
button2 = Button("Print Hello World", 20, 100, 200, True)
zone = Zone((0, 0, 100, 100), hello_world, spooky, ghosts, lift)
button2.bind(zone)
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
    button2.render(screen, m)
    zone.update(m)
    clock.tick(60)

pygame.quit()