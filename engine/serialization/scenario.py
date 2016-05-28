"""Implements the EventDataManager class"""
from engine.serialization.dmanager import DataManager
from engine.game.dungeon.event import Event

class EventDataManager(DataManager):
    """Singleton class used to get and assign event data"""

    def __init__(self):
        super().__init__("data/scenario.p")

    def events(self):
        return self.get()

    def new_event(self, name, floor, room):
        event = Event(name)
        self.events()[floor][room].append(event)

    def delete_event(self, name, floor, room):
        change_event = None
        for event in self.events()[floor][room]:
            if event.name == name:
                change_event = event
                break

        if change_event is not None:
            self.events()[floor][room].remove(change_event)

    def update_event_name(self, name, floor, room, new_name):
        for event in self.events()[floor][room]:
            if event.name == name:
                event.name = new_name
                break

    def update_event_floor(self, name, floor, room, new_floor):
        change_event = None
        for event in self.events()[floor][room]:
            if event.name == name:
                change_event = event
                break

        if change_event is not None:
            self.events()[floor][room].remove(change_event)
            self.events()[new_floor][room].append(change_event)

    def update_event_room(self, name, floor, room, new_room):
        change_event = None
        for event in self.events()[floor][room]:
            if event.name == name:
                change_event = event
                break

        if change_event is not None:
            self.events()[floor][room].remove(change_event)
            self.events()[floor][new_room].append(change_event)

    def add_dialogue(self, name, floor, room, dialogue):
        for event in self.events()[floor][room]:
            if event.name == name:
                event.dialogues[dialogue.name] = dialogue
                break

    def delete_dialogue(self, name, floor, room, dialogue_name):
        for event in self.events()[floor][room]:
            if event.name == name:
                del event.dialogues[dialogue_name]
                break

    def add_floor_type(self, floor):
        self.events()[floor] = {
            "monster" : [],
            "event" : [],
            "entrance" : [],
            "exit" : []
        }