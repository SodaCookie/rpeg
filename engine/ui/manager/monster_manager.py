"""Defines the monster renderer."""
import pygame

from engine.ui.core.manager import Manager
from engine.ui.core.zone import Zone
import engine.ui.element as element

class MonsterManager(Manager):
    """Manager for the monster class"""

    def __init__(self, monster, x, y):
        super(MonsterManager, self).__init__()
        SCALE = 4
        self.monster = monster
        self.highlight = False

        # zone interaction
        self.neutral = self.monster.surface# this is super hacky I DONT LIKE

        # monster image
        image = pygame.image.load(monster.surface).convert_alpha()
        image = pygame.transform.scale(image,
            (image.get_width()*SCALE, image.get_height()*SCALE))
        self.renderables.append((element.Image(image, x-image.get_width()//2, y-image.get_height())))

        # name
        self.name = element.Text(monster.name.title(), 20, x, y-image.get_height()-50)
        self.name.x = x - self.name.surface.get_width()//2
        self.renderables.append(self.name)
        self.hover_name = element.Text.draw(monster.name.title(), 20, (255, 255, 0),
            None, element.Text.LEFT)
        self.neutral_name = self.name.surface

        # bars
        self.health = element.Bar(32*SCALE, 2*SCALE, (116, 154, 104), x-16*SCALE , y-image.get_height()-20)
        self.action = element.Bar(32*SCALE, 2*SCALE, (212, 196, 148), x-16*SCALE, y-image.get_height()-5)
        health_missing = element.Bar(32*SCALE, 2*SCALE, (30, 30, 30), x-16*SCALE,  y-image.get_height()-20)
        action_missing = element.Bar(32*SCALE, 2*SCALE, (30, 30, 30), x-16*SCALE,  y-image.get_height()-5)
        self.renderables.append(health_missing)
        self.renderables.append(action_missing)
        self.renderables.append(self.health)
        self.renderables.append(self.action)

    def update(self, game):
        super().update(game)
        self.health.percent = 100*self.monster.get_cur_health()/ \
            self.monster.get_stat("health")
        self.action.percent = 100*self.monster.action/ \
            self.monster.action_max

    def on_click(self, game):
        pass

    def render(self, surface, game):
        if self.highlight:
            self.name.surface = self.hover_name
        else:
            self.name.surface = self.neutral_name
        super().render(surface, game)

    def __hash__(self):
        """This object is hashed by its name"""
        return hash(self.monster.name)