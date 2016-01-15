"""Defines the character renderer."""
from functools import partial
import random

import pygame

from engine.game.monster.monster import Monster
from engine.ui.core.manager import Manager
from engine.ui.core.zone import Zone
from engine.game.item.item import Item
from engine.game.action.action import ACTIONS
import engine.ui.element as element


__all__ = ["ScenarioManager"]

class ScenarioManager(Manager):
    """ScenarioManager handles the event dialogs that happen"""

    def __init__(self, x, y):
        super(ScenarioManager, self).__init__()
        SCALE = 4
        self.x = x
        self.y = y
        self.window = element.Window(500, 400, x, y)
        self.title = None
        self.dialog = None
        self.location = None

    def update(self, game):
        """Updates the scenario variables when changing rooms"""
        if game.current_location != self.location: # new event every move
            game.current_location.generate() # maybe moved elsewhere
            self.update_location(game.current_location)
            game.current_dialog = game.current_location.get_event()
            self.location = game.current_location
        if game.current_dialog != self.dialog:
            self.update_dialog(game, game.current_dialog)
            self.dialog = game.current_dialog
        super().update(game)

    def update_location(self, location):
        """Update the title of the body"""
        self.title = element.Text(location.get_event_name().title(), 30,
                                  self.x, self.y-34, (255, 255, 255), 500)

    def update_dialog(self, game, dialog):
        """Update the choices"""
        self.renderables = []
        self.zones = []
        if dialog == None: # clear and do nothing if no dialog
            return
        self.renderables.append(self.window)
        self.renderables.append(self.title)
        body = element.Text(dialog.body, 18, self.x+10, self.y+10,
                            (255, 255, 255), 480)
        self.renderables.append(body)
        height_counter = body.surface.get_height()+20
        for choice in dialog.get_choices(game.party.players):
            next_dialog = dialog.make_choice(choice)
            on_click = partial(self.on_choice_click, next_dialog)
            button = element.Button(choice, 18, self.x+10,
                self.y+height_counter)
            zone = Zone(((self.x+10, self.y+height_counter),
                button.surface.get_size()), on_click)
            button.bind(zone)
            self.zones.append(zone)
            self.renderables.append(button)
            height_counter += zone.rect.h

        if not dialog.get_choices(game.party.players):
            button = element.Button("Next", 18, self.x+10,
                self.y+height_counter)
            on_click = partial(self.on_no_choice_click, dialog)
            zone = Zone(((self.x+5, self.y+height_counter),
                button.surface.get_size()), on_click)
            button.bind(zone)
            self.zones.append(zone)
            self.renderables.append(button)

    @staticmethod
    def on_choice_click(dialog, game):
        game.current_dialog = dialog

    @staticmethod
    def on_no_choice_click(dialog, game):
        """We are done so we will exit also will execute some action"""
        game.current_dialog = None
        game.focus_window = None
        game.selected_player = None
        # Parse action
        # action := <type> [<parameter-name>:<parameter> <para...]
        for action in dialog.action:
            action_data = action.split(" ")
            action_type = action_data[0]
            kwargs = {action.split(":")[0]: action.split(":")[1] \
                for action in action_data[1:]}
            ACTIONS[action_type](game, **kwargs)