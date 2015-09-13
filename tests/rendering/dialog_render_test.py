import pygame

from engine.ui.manager.event_manager import EventManager
from engine.game.player.player import Player
from engine.game.dungeon.location import Location

class MockGameObject:
    mouse_x = 0
    mouse_y = 0
    mouse_button = (0, 0, 0)
    current_location = None
    current_dialog = None
    party = []

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
location = Location("entrance", 1)
m = MockGameObject()
m.current_location = location
m.party = [Player("Player") for i in range(3)]
event_manager = EventManager(100, 100)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    m.mouse_x, m.mouse_y = pygame.mouse.get_pos()
    m.mouse_button = pygame.mouse.get_pressed()
    screen.fill((0, 0, 0))
    event_manager.update(m)
    event_manager.render(screen, m)
    clock.tick(60)

pygame.quit()