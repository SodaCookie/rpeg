#! python3.2
import pygame

from engine.game.game import Game
from engine.game.event_handler import EventHandler
from engine.ui.manager.game_manager import GameManager

pygame.init()

screen = pygame.display.set_mode((1280, 720))
game = Game()
manager = GameManager()
manager.init(game, "normal")
event = EventHandler()
clock = pygame.time.Clock()
running = True

while running:
    running = event.update(game)
    manager.update(game)
    screen.fill((0, 0, 0))
    manager.render(screen, game)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()