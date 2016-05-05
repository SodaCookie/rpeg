"""Defines the Event object"""

class Event(object):
    """A simple container class to store information concerning
    the an event class"""

    def __init__(self, name):
        """Constructs an Event object.
        Takes a name to name an event, a room_type to associate with
        a room_type for a location, a floor_type to associate with a
        floor and the root of a dialogue tree."""
        super().__init__()
        self.name = name
        self.dialogues = {}

    def add_dialogue(self, dialogue):
        self.dialogues[dialogue.name] = dialogue
        dialogue.event = self