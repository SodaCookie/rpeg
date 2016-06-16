"""Implements the UI System"""
import random

import pygame
import anime

from engine.system import System, Message
from engine.ui.draw.simple import draw_text
import engine.ui.manager as manager

class AnimationSystem(System):
    """System responsible for handling game related events"""

    def __init__(self, game):
        super().__init__(game, "animation")

    def init(self, game):
        self.animations = []
        self.message_font = pygame.font.Font(
            "assets/fonts/VT323-Regular.ttf", 24)
        self.battle_font = pygame.font.Font(
            "assets/fonts/VT323-Regular.ttf", 40)

    def update(self, delta, game):
        messages = self.flush_messages()
        for message in messages:
            self.dispatch(message, game)

        surface = pygame.display.get_surface()
        for animation in self.animations[:]:
            animation.update()
            animation.render(surface)
            if not animation.is_dirty():
                self.animations.remove(animation)

    def dispatch(self, message, game):
        """Function for determining what action to call depending on the
        message"""
        width, height = pygame.display.get_surface().get_size()
        if message.mtype == "message":
            # Set hovered object from a slot
            text, colour = message.args
            surface = draw_text(text, self.message_font, colour)
            animation = anime.Anime(surface, width // 2, 500)
            animation.set_filter('y', anime.filter.linear, 2)
            animation.set_filter('opacity', anime.filter.linear, 5)
            animation.y = 400
            animation.opacity = 0
            self.animations.append(animation)
        elif message.mtype == "battle-message":
            target, text, colour= message.args
            x = random.randint(-20, 20)
            y = random.randint(-20, 20)
            if target in game.party.players:
                index = game.party.players.index(target)
                x = x + 156 + 312 * index
                y = y + height - 100
            elif game.encounter and target in game.encounter:
                index = game.encounter.index(target)
                num_enemies = len(game.encounter)
                x = x + width // (num_enemies + 1) * (index + 1)
                y = y + 200

            surface = draw_text(text, self.battle_font, colour)
            animation = anime.Anime(surface, x, y)
            animation.set_filter('y', anime.filter.linear, 1)
            animation.set_filter('opacity', anime.filter.linear, 4)
            animation.y = y - 100
            animation.opacity = 0
            self.animations.append(animation)


