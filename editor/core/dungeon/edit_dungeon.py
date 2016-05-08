from data.scenarios import EVENTS

def create(name):
    EVENTS[name] = {}

def set_name(old_name, new_name):
    EVENTS[new_name] = EVENTS[old_name]
    del EVENTS[old_name]

def delete(name):
    del EVENTS[name]