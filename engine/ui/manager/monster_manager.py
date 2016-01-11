"""Defines the monster renderer."""
import pygame

from engine.ui.core.manager import Manager
from engine.ui.core.zone import Zone
import engine.ui.element as element

class MonsterManager(Manager):
    """Manager for the monster class"""

    def __init__(self, monster, x, y):
        super(MonsterManager, self).__init__()
        SCALE = 4 # TEMPORARY VARIABLE
        self.monster = monster
        self.highlight = False

        # Load monster neutral image
        raw_image = pygame.image.load( \
            monster.graphic["neutral"]).convert_alpha()
        raw_image = pygame.transform.scale(raw_image, \
            (raw_image.get_width()*SCALE, raw_image.get_height()*SCALE))

        # Create image element
        self.image_element = element.Image(raw_image,
            x-raw_image.get_width()//2, y-raw_image.get_height())
        self.renderables.append(self.image_element)

        # Store raw image
        self.neutral_image = raw_image

        # Load monster hover image
        raw_image = pygame.image.load(
            monster.graphic["hover"]).convert_alpha()

        # Store hover image
        self.hover_image = pygame.transform.scale(raw_image,
            (raw_image.get_width()*SCALE, raw_image.get_height()*SCALE))

        # Create text element
        self.text_element = element.Text(monster.name.title(), 20, x, y-self.image.get_height()-75)
        self.text_element.x = x - self.text_element.surface.get_width()//2
        self.renderables.append(self.text_element)

        # Store hovered and neutral text surfaces
        self.neutral_name = self.text_element.surface
        self.hover_name = element.Text.draw(monster.name.title(), 20,
            (255, 255, 0), None, element.Text.LEFT)

        # Create health and action bars
        self.health_bar = element.Bar(32*SCALE, 2*SCALE, (116, 154, 104),
            x-16*SCALE , y-self.image.get_height()-40)
        self.action_bar = element.Bar(32*SCALE, 2*SCALE, (212, 196, 148),
            x-16*SCALE, y-self.image.get_height()-25)
        health_missing = element.Bar(32*SCALE, 2*SCALE, (30, 30, 30),
            x-16*SCALE,  y-self.image.get_height()-40)
        action_missing = element.Bar(32*SCALE, 2*SCALE, (30, 30, 30),
            x-16*SCALE,  y-self.image.get_height()-25)
        self.renderables.append(health_missing)
        self.renderables.append(action_missing)
        self.renderables.append(self.health_bar)
        self.renderables.append(self.action_bar)

    def update(self, game):
        super().update(game)
        self.health_bar.percent = 100*self.monster.get_cur_health()/ \
            self.monster.get_stat("health")
        self.action_bar.percent = 100*self.monster.action/ \
            self.monster.action_max

    def on_click(self, game):
        if game.selected_move and not self.monster.fallen:
            game.selected_target = self.monster

    def render(self, surface, game):
        if self.monster.fallen:
            return
        if self.highlight:
            self.text_element.surface = self.hover_name
            self.image_element.surface = self.hover_image
        else:
            self.text_element.surface = self.neutral_name
            self.image_element.surface = self.neutral_image
        super().render(surface, game)

    def __hash__(self):
        """This object is hashed by its name"""
        return hash(self.monster.name)