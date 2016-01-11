from functools import partial

import pygame

from engine.ui.core.manager import Manager
from engine.ui.manager.monster_manager import MonsterManager
from engine.ui.core.zone import Zone

class EncounterManager(Manager):
    """The EncounterManager manages the Monsters in an encounter
    it is in charge of proper highlighting and binding of monsters to
    zones"""

    def __init__(self):
        super(EncounterManager, self).__init__()
        self.monster_managers = []

    def update(self, game):
        """Overrides zones update to dictionary for removing"""
        super().update(game)
        for manager in self.monster_managers:
            manager.update(game)

        game_set = set(game.encounter)
        cur_set = set(m.monster for m in self.monster_managers)

        if game_set.symmetric_difference(cur_set):
            self.monster_managers = []
            self.zones = []
            for i, char in enumerate(game_set):
                x = pygame.display.get_surface().get_width()//len(game_set)*(i+1)-pygame.display.get_surface().get_width()//len(game_set)//2
                y = pygame.display.get_surface().get_height()-400
                mm = MonsterManager(char, x, y)
                self.monster_managers.append(mm)
                # create a new zone for that manager
                # bind on_hover to this manager
                on_hover = partial(self.on_hover, mm)
                off_hover = partial(self.off_hover, mm)
                coordx = x - mm.image_element.surface.get_size()[0]//2
                coordy = y - mm.image_element.surface.get_size()[1]
                z = Zone(((coordx, coordy),
                    mm.image_element.surface.get_size()),
                    mm.on_click, on_hover, off_hover)
                self.zones.append(z)

    def render(self, surface, game):
        if game.encounter:
            super().render(surface, game)
            for c in self.monster_managers:
                c.render(surface, game)

    @staticmethod
    def on_hover(manager, game):
        manager.highlight = True

    @staticmethod
    def off_hover(manager, game):
        manager.highlight = False