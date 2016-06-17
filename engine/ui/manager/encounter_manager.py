from functools import partial
from itertools import zip_longest

import pygame

from engine.ui.core.manager import Manager
import engine.ui.element as element

class EncounterManager(Manager):
    """The EncounterManager manages the Monsters in an encounter
    it is in charge of proper highlighting and binding of monsters to
    zones"""

    def __init__(self, x, y):
        super().__init__("encounter", x, y)
        self.encounter = None
        self.monster_elements = []
        for i in range(4):
            monster = element.MonsterCard("monster-%d" % i, x, y, None)
            self.monster_elements.append(monster)
            self.add_renderable(monster)

    def set_encounter(self, encounter):
        width = pygame.display.get_surface().get_width()
        pairs = list(zip_longest(encounter, self.monster_elements,
            fillvalue=None))
        monsters_len = len(encounter)
        for i, pair in enumerate(pairs):
            monster, elem = pair
            elem.set_monster(monster)
            elem.move(width // (monsters_len + 1) * (i + 1), self.y)

        # if game_set.symmetric_difference(cur_set):
        #     self.monster_managers = []
        #     self.zones = []
        #     for i, char in enumerate(game_set):
                # x = pygame.display.get_surface().get_width()//len(game_set)*(i+1)-pygame.display.get_surface().get_width()//len(game_set)//2
        #         y = pygame.display.get_surface().get_height()-400
        #         mm = MonsterManager(char, x, y)
        #         self.monster_managers.append(mm)


    def update(self, game, system):
        """Overrides zones update to dictionary for removing"""
        if self.encounter != game.encounter:
            self.set_encounter(game.encounter)
            self.encounter = game.encounter
