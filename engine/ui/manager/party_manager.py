from functools import partial

import pygame

from engine.ui.core.manager import Manager
from engine.ui.manager.character_manager import CharacterManager
from engine.ui.core.zone import Zone

class PartyManager(Manager):
    """PartyManager manages all render and updating to the party
    not the individual character. It is in charge of adding and
    removing character managers throughout the game"""

    def __init__(self):
        super(PartyManager, self).__init__()
        self.char_managers = []

    def update(self, game):
        super().update(game)
        for manager in self.char_managers:
            manager.update(game)

        game_set = set(game.party.players)
        cur_set = set(c.character for c in self.char_managers)

        if game_set.symmetric_difference(cur_set):
            self.char_managers = []
            self.zones = []
            for i, char in enumerate(game_set):
                x = i*300+20
                y = pygame.display.get_surface().get_height()-164-20
                cm = CharacterManager(char, x, y)
                self.char_managers.append(cm)
                # create a new zone for that manager
                # bind on_hover to this manager
                on_hover = partial(self.on_hover, cm)
                off_hover = partial(self.off_hover, cm)
                z = Zone(((x, y), cm.window.surface.get_size()), cm.on_click,
                        on_hover, off_hover)
                self.zones.append(z)

    def render(self, surface, game):
        super().render(surface, game)
        for c in self.char_managers:
            c.render(surface, game)

    @staticmethod
    def on_hover(manager, game):
        manager.highlight = True

    @staticmethod
    def off_hover(manager, game):
        manager.highlight = False