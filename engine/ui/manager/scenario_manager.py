"""Defines the character renderer."""
from functools import partial
import random

import pygame

from engine.game.monster.monster import Monster
from engine.ui.core.manager import Manager
from engine.ui.core.zone import Zone
from engine.game.item.item import Item
import engine.ui.element as element

__all__ = ["ScenarioManager"]

def action_nothing(game, **kwargs):
    """Does nothing"""
    pass

def action_battle(game, **kwargs):
    """Implements a battle"""
    defaults = {
        "challenge" : random.randint(8, 12), # TO FIX
        "monsters" : None
    }
    defaults.update(kwargs)
    if defaults["monsters"] == None:
        names = []
        while defaults["challenge"] > 0 and len(names) < 3:
            valid_monsters = [(name, monster["rating"])
                for name, monster in Monster.MONSTERS.items()
                if monster["rating"] <= defaults["challenge"] and\
                monster["location"] == game.floor_type]
            if not valid_monsters:
                break #failsafe
            name, rating = random.choice(valid_monsters)
            names.append(name)
            defaults["challenge"] -= rating
        if defaults["challenge"]:
            valid_monsters = [(name, monster["rating"])
                for name, monster in Monster.MONSTERS.items()
                if monster["rating"] <= defaults["challenge"] and\
                monster["location"] == game.floor_type]
            if valid_monsters:
                highest_value = 0
                for name, value in valid_monsters:
                    if value > highest_value:
                        highest_value = value
            valid_names = [name for name, value in valid_monsters
                           if value == highest_value]
            names.append(random.choice(valid_names))
        defaults["monsters"] = [Monster(name) for name in names]
    else:
        names = defaults["monsters"]
        defaults["monsters"] = [Monster(name) for name in names]
    monsters = [Monster(**defaults) for i in range(defaults["number"])]
    game.encounter = defaults["monsters"]

def action_loot(game, **kwargs):
    """Gives party loot"""
    defaults = {
        "reward-tier" : "low"
        "shard" : None,
        "item" : None
    }
    defaults.update(kwargs)
    # Handle unspecified shard
    if defaults["shard"] == None: # arbitrary
        if defaults["reward-tier"] == "low":
            defaults["shard"] = game.floor_level * random.randint(15, 20)
        elif defaults["reward-tier"] == "medium":
            defaults["shard"] = game.floor_level * random.randint(30, 35)
        elif defaults["reward-tier"] == "high":
            defaults["shard"] = game.floor_level * random.randint(50, 70)
    # Handle unspecified item
    if defaults["item"] == None:
        defaults["item"] = []
        parameters = {
            "floor": game.floor_level,
            "floor-type": game.floor_type
        }
        if "reward-tier" == "medium":
            if random.randint(0, 99) < 50:
                defaults.append(Item(**parameters))
        elif "reward-tier" == "high":
            game.floor_level * random.randint(50, 70)
            if random.randint(0, 99) < 30:
                defaults.append(Item(**parameters))
    # Handle raw input as a string for item
    else:
        # item := <name>,<parameter>|[<more parameters>]@[<item>]
        items = defaults["item"]
        defaults["item"] = []
        if items:
            for item_parameters in items.split("@"):
                # to be fed into the builders
                parameters = {
                    "floor": game.floor_level,
                    "floor-type": game.floor_type
                }
                for parameter in item_parameters.split("|"):
                    parameter_name = parameter.split(",")[0]
                    parameter_value = parameter.split(",")[1]
                    parameters[parameter_name] = parameter_value
                defaults["item"].append(Item(**parameters))
    game.loot = (defaults["shards"], defaults["item"])
    game.focus_window = "loot"

ACTIONS = {
    "" : action_nothing,
    "battle" : action_battle,
    "loot" : action_loot
}

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