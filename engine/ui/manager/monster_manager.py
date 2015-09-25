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
        self.image = pygame.image.load(monster.surface).convert_alpha()
        self.image = pygame.transform.scale(self.image,
            (self.image.get_width()*SCALE, self.image.get_height()*SCALE))
        self.monster_image = element.Image(self.image, x-self.image.get_width()//2, y-self.image.get_height())
        self.renderables.append(self.monster_image)
        self.neutral_image = self.monster_image.surface

        self.hover_image = pygame.image.load(self.monster.hover).convert_alpha()
        self.hover_image = pygame.transform.scale(self.hover_image,
            (self.hover_image.get_width()*SCALE, self.hover_image.get_height()*SCALE))

        # name
        self.name = element.Text(monster.name.title(), 20, x, y-self.image.get_height()-75)
        self.name.x = x - self.name.surface.get_width()//2
        self.renderables.append(self.name)
        self.hover_name = element.Text.draw(monster.name.title(), 20, (255, 255, 0),
            None, element.Text.LEFT)
        self.neutral_name = self.name.surface

        # bars
        self.health = element.Bar(32*SCALE, 2*SCALE, (116, 154, 104), x-16*SCALE , y-self.image.get_height()-40)
        self.action = element.Bar(32*SCALE, 2*SCALE, (212, 196, 148), x-16*SCALE, y-self.image.get_height()-25)
        health_missing = element.Bar(32*SCALE, 2*SCALE, (30, 30, 30), x-16*SCALE,  y-self.image.get_height()-40)
        action_missing = element.Bar(32*SCALE, 2*SCALE, (30, 30, 30), x-16*SCALE,  y-self.image.get_height()-25)
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
        if game.selected_move:
            game.selected_target = self.monster

    def render(self, surface, game):
        if self.monster.fallen:
            return
        if self.highlight:
            self.name.surface = self.hover_name
            self.monster_image.surface = self.hover_image
        else:
            self.name.surface = self.neutral_name
            self.monster_image.surface = self.neutral_image
        super().render(surface, game)

    def __hash__(self):
        """This object is hashed by its name"""
        return hash(self.monster.name)