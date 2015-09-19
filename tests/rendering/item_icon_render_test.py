import pygame

import engine.game.item.item as Item
from engine.ui.element.item_icon import ItemIcon
from engine.ui.core.zone import Zone

class MockGameObject:
    mouse_x = 0
    mouse_y = 0
    mouse_button = (0, 0, 0)
    selected_player = None

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
m = MockGameObject()
itm = Item.Item(rarity="legendary", floor=5)
icn = ItemIcon(itm, 300, 300)
z = Zone((300, 300, 50, 50), None)
icn.bind(z)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    m.mouse_x, m.mouse_y = pygame.mouse.get_pos()
    m.mouse_button = pygame.mouse.get_pressed()
    screen.fill((0, 0, 0))
    z.update(m)
    icn.render(screen, m)
    clock.tick(60)

pygame.quit()