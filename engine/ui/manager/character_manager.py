"""Defines the character renderer."""
import pygame

from engine.ui.core.manager import Manager
from engine.ui.core.zone import Zone
import engine.ui.element as element

class CharacterManager(Manager):
    """Manager for the character class"""

    def __init__(self, character, x, y):
        super(CharacterManager, self).__init__()
        SCALE = 4
        self.character = character
        self.highlight = False
        # name
        self.name = element.Text(character.name, 20, x, y-20)
        self.renderables.append(self.name)
        self.hover_name = element.Text.draw(character.name, 20, (255, 255, 0),
            None, element.Text.LEFT)
        self.neutral_name = self.name.surface
        # window
        self.window = element.Window(280, 156, x, y+4)
        self.neutral = self.window.surface
        self.hover = element.Window.highlight_window(
            self.window.surface, (255, 255, 0)) # yellow
        self.renderables.append(self.window)

        # portrait
        portrait = pygame.image.load(character.portrait).convert_alpha()
        portrait = pygame.transform.scale(portrait,
            (portrait.get_width()*SCALE, portrait.get_height()*SCALE))
        self.renderables.append((element.Image(portrait, x, y)))

        # bars
        self.health = element.Bar(32*SCALE, 2*SCALE, (116, 154, 104), x+140, y+20)
        self.action = element.Bar(32*SCALE, 2*SCALE, (212, 196, 148), x+140, y+36)
        health_missing = element.Bar(32*SCALE, 2*SCALE, (30, 30, 30), x+140, y+20)
        action_missing = element.Bar(32*SCALE, 2*SCALE, (30, 30, 30), x+140, y+36)
        self.renderables.append(health_missing)
        self.renderables.append(action_missing)
        self.renderables.append(self.health)
        self.renderables.append(self.action)

    def update(self, game):
        super().update(game)
        self.health.percent = 100*self.character.get_cur_health()/ \
            self.character.get_stat("health")
        self.action.percent = 100*self.character.action/ \
            self.character.action_max

    def on_click(self, game):
        if game.selected_player:
            if game.selected_player.selected_move and \
                    not game.selected_player.target:
                game.selected_player.selected_move = None
            game.selected_player = self.character
        else:
            game.selected_player = self.character

    def render(self, surface, game):
        if self.highlight:
            self.window.surface = self.hover
            self.name.surface = self.hover_name
        else:
            self.window.surface = self.neutral
            self.name.surface = self.neutral_name
        super().render(surface, game)

    def __hash__(self):
        """This object is hashed by its name"""
        return hash(self.character.name)