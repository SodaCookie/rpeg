"""Implements the UI System"""
import logging
from collections import OrderedDict

import pygame

from engine.system import System, Message
import engine.ui.manager as manager

class UISystem(System):
    """System responsible for handling game related events"""

    layouts = {
        "scenario" : ["background", "party", "scenario"],
        "default" : ["background", "party", "castbar", "sidebar"],
        "character" : ["background", "party", "castbar", "sidebar",
                       "character", "party-info"],
        "battle" : ["background", "party", "castbar", "encounter"],
        "travel" : ["background", "party", "travel", "sidebar"],
        "loot" : ["background", "party", "loot", "sidebar", "party-info"],
        "level" : ["background", "level"]
    }

    def __init__(self, game):
        super().__init__(game, "ui")
        self.managers = OrderedDict()
        self.image_stack = []
        self.rendering = []

    def init(self, game):
        width, height = pygame.display.get_surface().get_size()
        self.managers["background"] = manager.BackgroundManager(
            "image/ui/catacomb-background-COPYRIGHTED.jpg")
        self.managers["party"] = manager.PartyManager(32, height - 204)
        self.managers["sidebar"] = manager.SideBarManager(0, 10, width)
        self.managers["encounter"] = manager.EncounterManager(0, 340)
        self.managers["castbar"] = manager.CastBarManager(
            width // 2 - (56 * 10 + 14) // 2, 440, 10)
        self.managers["loot"] = manager.LootManager(
            width // 2 - 400, 72, 552, 348)
        self.managers["scenario"] = manager.ScenarioManager(
            width // 2 - 300, 52, 600, 400)
        self.managers["travel"] = manager.TravelManager(
            width // 2 - 400, 72, 800, 348)
        self.managers["level"] = manager.LevelUpManager()
        self.managers["character"] = manager.CharacterManager(
            width // 2 - 400, 72, 552, 348)
        self.managers["party-info"] = manager.PartyInfoManager(
            width // 2 + 162, 72, 260, 348, game)
        self.rendering = self.layouts["scenario"]

    def update(self, delta, game):
        messages = self.flush_messages()
        for message in messages:
            self.dispatch(message, game)

        # Render Managers
        surface = pygame.display.get_surface()
        surface.fill((0, 0, 0))
        for manager in self.rendering:
            self.managers[manager].render(surface, game, self.game)

    def set_layout(self, layout):
        self.rendering = self.layouts[layout]

    def dispatch(self, message, game):
        """Function for determining what action to call depending on the
        message"""
        if message.mtype == "layout": # Travels the part
            layout = message.args[0]
            self.set_layout(layout)
        elif message.mtype == "toggle":
            manager = message.args[0]
            if manager in self.rendering:
                self.rendering.remove(manager)
            else:
                self.rendering.append(manager)
        elif message.mtype == "load-moves":
            moves = message.args[0]
            self.managers["level"].load_moves(moves)
        elif message.mtype == "refresh-character":
            self.managers["character"].set_player(
                self.managers["character"].character)
        elif message.mtype == "push-bg":
            surface = self.managers["background"].get_image()
            self.image_stack.append(surface)
            new_surface = pygame.display.get_surface().copy()
            if len(message.args) == 1:
                new_surface.fill(message.args[0],
                    special_flags=pygame.BLEND_ADD)
            elif len(message.args) == 2:
                new_surface.fill(message.args[0],
                    special_flags=message.args[1])
            self.managers["background"].set_image(new_surface)
        elif message.mtype == "pop-bg":
            if len(self.image_stack) > 0:
                self.managers["background"].set_image(self.image_stack.pop(-1))
            else:
                logging.warning("Background was popped with an empty stack")