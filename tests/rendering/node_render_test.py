import pygame

from engine.ui.element.travel_node import TravelNode
from engine.ui.core.zone import Zone

class MockGameObject:
    mouse_x = 0
    mouse_y = 0
    mouse_button = (0, 0, 0)

def hello_world(game):
    print("Jello World!")

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
node1 = TravelNode("unknown", 100, 100, True)
node2 = TravelNode("visited", 200, 100)
zone = Zone((100, 100, 27, 27), hello_world)
node1.bind(zone)
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
    node1.render(screen, m)
    node2.render(screen, m)
    zone.update(m)
    clock.tick(60)

pygame.quit()