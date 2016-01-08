import pygame

from engine.game.item.item import Item
from engine.ui.manager.loot_manager import LootManager

class MockGameObject:
    mouse_x = 0
    mouse_y = 0
    loot = None
    mouse_button = (0, 0, 0)
    focus_window = "loot"

pygame.init()
screen = pygame.display.set_mode((1280, 720))
loot = LootManager(100, 100, 300, 410)
clock = pygame.time.Clock()
m = MockGameObject()
m.loot = (100, 100, [Item(rarity="legendary"), Item()]) # gold, experience, itesms

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    m.mouse_x, m.mouse_y = pygame.mouse.get_pos()
    m.mouse_button = pygame.mouse.get_pressed()
    screen.fill((0, 0, 0))
    loot.update(m)
    loot.render(screen, m)
    clock.tick(60)

pygame.quit()