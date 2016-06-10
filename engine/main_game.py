"""Defines the Game object"""
from collections import OrderedDict

import pygame

from engine.game.game_object import GameObject

class Game(object):

    def __init__(self):
        super().__init__()
        self.systems = OrderedDict()
        self.running = True
        self.prevtime = 0

    def add_system(self, system):
        self.systems[system.name] = system

    def run(self):
        """Run the game"""

        # Initiate pygame, screen, game object, clock
        pygame.init()
        screen = pygame.display.set_mode((1280, 720))
        game = GameObject()
        clock = pygame.time.Clock()
        for system in self.systems:
            self.systems[system].init(game)

        # Game loop
        while self.running:
            delta = pygame.time.get_ticks() - self.prevtime
            self.prevtime = pygame.time.get_ticks()
            for system in self.systems:
                self.systems[system].update(delta, game)
            pygame.display.flip()
            clock.tick(60)

        for system in self.systems:
            self.systems[system].quit(game)
        pygame.quit()

    def message(self, system, message):
        """Sends a message to another system by name. Takes a system name
        as a string and the message object to pass."""
        self.systems[system].message(message)

    def quit(self):
        """Tells the system to quit on the next game loop"""
        self.running = False