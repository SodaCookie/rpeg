"""Defines the character renderer."""
from functools import partial
import random

import pygame

from engine.system import Message
from engine.ui.core.manager import Manager
import engine.ui.element as element

__all__ = ["ScenarioManager"]

class ScenarioManager(Manager):
    """ScenarioManager handles the event dialogs that happen"""

    def __init__(self, x, y, width, height):
        super().__init__("scenario", x, y)
        self.title = element.Text("event-title", x, y, "", 36,
            width=width, justify="left")
        self.body = element.Text("event-body", x + 12, y + 48, "", 18,
            width=width - 24, justify="left")
        self.choice_elements = []
        self.location = None
        self.dialogue = None
        self.width = width
        self.height = height

        self.add_renderable(element.Frame("frame", x, y + 40, width,
            height - 20))
        self.add_renderable(self.title)
        self.add_renderable(self.body)

    def update(self, game, system):
        """Updates the scenario variables when changing rooms"""
        if game.current_location != self.location: # new event every move
            self.update_location(game.current_location)
            self.location = game.current_location
        if game.current_dialogue != self.dialogue:
            self.update_dialogue(game, game.current_dialogue)
            self.dialogue = game.current_dialogue
        super().update(game, system)

    def update_location(self, location):
        """Update text of the body"""
        self.title.set_text(location.get_event_name())

    def update_dialogue(self, game, dialogue):
        """Update the main body to reflect the current dialogue"""
        if dialogue is None:
            return

        # Update body
        dialogue = game.current_location.get_dialogue(dialogue)
        self.body.set_text(dialogue.body)
        self.body.refresh(game) # Draw now
        height = self.body.get_height() + 60

        # Clear previous choice elements
        for elem in self.choice_elements:
            self.remove_renderable(elem.name)
        self.choice_elements = []

        # Get current choices
        choices = dialogue.get_available_choices(game.party)

        # Add a corresponding button for every choice
        for i, choice in enumerate(choices):
            choice_dialogue = game.current_location.get_dialogue(choice)
            # on_click = partial(self.on_choice_click, choice)
            button = element.Button("button-%d" % i,
                self.on_choice_click(choice),
                x = self.x + 12,
                y = self.y + height,
                size = 18,
                text = "%d. " % (i + 1) + choice_dialogue.dtext,
                justify = "left",
                vjustify = "up",
                width = self.width - 24,
                windowed = False)
            self.choice_elements.append(button)
            self.add_renderable(button)
            height += button.get_height()

        # If there are no choices add a next button
        if not choices:
            button = element.Button("next",
                self.on_no_choice_click(dialogue),
                x = self.x + 12,
                y = self.y + height,
                size = 18,
                text = "Next",
                justify = "left",
                vjustify = "up",
                width = self.width - 24,
                windowed = False)
            self.choice_elements.append(button)
            self.add_renderable(button)

    def on_choice_click(self, dialogue):
        def on_click(game, system):
            system.message("game", Message("dialogue", dialogue))
        return on_click

    def on_no_choice_click(self, dialogue):
        """We are done so we will exit also will execute some action"""
        def on_click(game, system):
            system.message("ui", Message("layout", "default"))
            system.message("game", Message("close-event"))
            system.message("game", Message("action", dialogue))
            self.dialogue = None
        return on_click
