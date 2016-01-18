from engine.game.item.item import Item

BASE_ITEMS = {}
ITEMS = {}

BASE_ITEMS["sword"] = Item(
    "wooden sword",
    "sword",
    "hand",
    {"attack": 3,
    "defense": 0,
    "magic": 0,
    "speed": 0,
    "health": 0})

BASE_ITEMS["shield"] = Item(
    "wooden shield",
    "shield",
    "hand",
    {"attack": 3,
    "defense": 0,
    "magic": 0,
    "speed": 0,
    "health": 0})