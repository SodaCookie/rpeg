"""Implements the UI System"""

import pygame

from engine.system import System, Message
import engine.ui.manager as manager

class UISystem(System):
    """System responsible for handling game related events"""

    def __init__(self, game):
        super().__init__(game, "ui")

    def init(self, game):
        self.hover = manager.MouseHoverManager()
        self.party = manager.PartyManager()
        self.sidebar = manager.SidebarManager()
        self.encounter = manager.EncounterManager()
        self.castbar = manager.CastBarManager(440)
        self.loot = manager.LootManager(450, 20, 300, 400)
        self.scenario = manager.ScenarioManager(20, 60)
        self.travel = manager.TravelManager(800, 300, 1280//2-800//2, 100)
        self.level = manager.LevelUpManager(1280, 720)
        self.shop = None
        self.character = manager.CharacterCardManager(20, 20)

    def update(self, delta, game):
        messages = self.flush_messages()
        for message in messages:
            self.dispatch(message)

        # Render Managers
        surface = pygame.display.get_surface()
        surface.fill((0, 0, 0))
        self.sidebar.render(surface, game)
        self.encounter.render(surface, game)
        self.party.render(surface, game)
        self.character.render(surface, game)
        self.loot.render(surface, game)
        self.castbar.render(surface, game)
        self.level.render(surface, game)
        if game.focus_window == "travel":
            self.travel.render(surface, game)
        elif game.focus_window == "shop":
            pass
        elif game.focus_window == "loot":
            pass
        elif game.focus_window == "scenario":
            self.scenario.render(surface, game)
        self.hover.render(surface, game)
        pygame.display.flip()

    def dispatch(self, message):
        pass