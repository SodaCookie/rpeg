import copy

from engine.game.monster.monster import Monster.MONSTERS as MONSTERS

def create(name):
    MONSTERS[name] =
    {
        "graphic": None,
        "location": None,
        "rating": 0,
        "stats":
        {
            "health": 0,
            "attack": 0,
            "defense": 0,
            "magic": 0,
            "resist": 0,
            "speed": 0,
            "action": 0
        },
        "abilities": [],
        "attributes": [],
        "unique": False
    }

def set_name(old_name, new_name):
    MONSTERS[new_name] = MONSTERS[old_name]
    del MONSTERS[old_name]

def update(name, graphic, location, rating, stats, abilities,
    attributes, unique):
    MONSTERS[name].update(
        {
            "graphic": graphic,
            "location": location,
            "rating": rating,
            "stats": stats
            "abilities": abilities,
            "attributes": attributes,
            "unique": unique
        })

def delete(name):
    del MONSTERS[name]
