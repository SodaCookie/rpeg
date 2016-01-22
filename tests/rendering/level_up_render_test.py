import pygame

from engine.game.player.player import Player
from engine.ui.manager.level_up_manager import LevelUpManager
from engine.game.move.built_moves import *

class MockGameObject:
    mouse_x = 0
    mouse_y = 0
    mouse_button = (0, 0, 0)
    focus_window = "level"
    selected_player = None

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
m = MockGameObject()
p = Player("Test")
p.add_move(PLAYER_MOVES["attack"])
p.roll_moves()
m.selected_player = p
lum = LevelUpManager(*screen.get_size())

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     if m.selected_player:
        #         m.selected_player = None
        #     else:
        #         m.selected_player = p
    pygame.display.flip()
    m.mouse_x, m.mouse_y = pygame.mouse.get_pos()
    m.mouse_button = pygame.mouse.get_pressed()
    screen.fill((255, 255, 255))
    lum.update(m)
    lum.render(screen, m)
    clock.tick(60)

pygame.quit()