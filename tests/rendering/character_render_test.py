import pygame

from engine.game.player.player import Player
from engine.ui.manager.character_manager import CharacterManager

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

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
m = MockGameObject()
p = Player("Player the Awesome")
cm = CharacterManager(p, 100, 100)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            cm.highlight = True
        elif event.type == pygame.MOUSEBUTTONUP:
            cm.highlight = False
    if p.action < 100:
        p.action += 1
    pygame.display.flip()
    m.mouse_x, m.mouse_y = pygame.mouse.get_pos()
    m.mouse_button = pygame.mouse.get_pressed()
    screen.fill((0, 0, 0))
    cm.update(m)
    cm.render(screen, m)
    clock.tick(60)

pygame.quit()