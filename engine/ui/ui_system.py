"""Implements the UI System"""
from collections import OrderedDict

import pygame

from engine.system import System, Message
import engine.ui.manager as manager

class UISystem(System):
    """System responsible for handling game related events"""

    def __init__(self, game):
        super().__init__(game, "ui")
        self.managers = OrderedDict()
        self.rendering = []

    def init(self, game):
        self.managers["test"] = manager.PlayerManager("test", 10, 10)
        # self.managers["hover"] = manager.MouseHoverManager()
        # self.managers["party"] = manager.PartyManager()
        # self.managers["sidebar"] = manager.SidebarManager()
        # self.managers["encounter"] = manager.EncounterManager()
        # self.managers["castbar"] = manager.CastBarManager(440)
        # self.managers["loot"] = manager.LootManager(450, 20, 300, 400)
        # self.managers["scenario"] = manager.ScenarioManager(20, 60)
        # self.managers["travel"] = manager.TravelManager(
        #     800, 300, 1280//2-800//2, 100)
        # self.managers["level"] = manager.LevelUpManager(1280, 720)
        # self.managers["character"] = manager.CharacterCardManager(20, 20)
        self.rendering = ["test"]

    def update(self, delta, game):
        messages = self.flush_messages()
        for message in messages:
            self.dispatch(message)

        # Render Managers
        surface = pygame.display.get_surface()
        surface.fill((0, 0, 0))
        for manager in self.rendering:
            self.managers[manager].render(surface, game, self.game)
        pygame.display.flip()

    def dispatch(self, message):
        pass