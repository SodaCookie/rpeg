from data.scenarios import EVENTS

def create(name, dungeon):
    EVENTS[dungeon][name] = []

def set_name(old_name, new_name, dungeon):
    EVENTS[dungeon][new_name] = EVENTS[dungeon][old_name]

def update(name, dungeon, dialogues):
    EVENTS[dungeon][name] = dialogues

def delete(name, dungeon):
    del EVENTS[dungeon][name]
