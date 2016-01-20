from engine.game.item.item import Item

BASE_ITEMS = {}
ITEMS = {}

# BASIC ITEM SEGMENT
BASE_ITEMS["sword"] = Item(
    "wooden sword",
    "hand",
    {"attack": 2,
    "defense": 0,
    "magic": 0,
    "resist": 0,
    "speed": 0,
    "health": 0,
    "action": 0})

BASE_ITEMS["shield"] = Item(
    "wooden shield",
    "hand",
    {"attack": 0,
    "defense": 2,
    "magic": 0,
    "resist": 0,
    "speed": 0,
    "health": 0,
    "action": 0})


BASE_ITEMS["wand"] = Item(
    "apprentice's wand",
    "hand",
    {"attack": 0,
    "defense": 0,
    "magic": 2,
    "resist": 0,
    "speed": 0,
    "health": 0,
    "action": 0})

BASE_ITEMS["head"] = Item(
    "leather cap",
    "head",
    {"attack": 0,
    "defense": 1,
    "magic": 0,
    "resist": 0,
    "speed": 0,
    "health": 0,
    "action": 0})


BASE_ITEMS["body"] = Item(
    "leather garbs",
    "body",
    {"attack": 0,
    "defense": 1,
    "magic": 0,
    "resist": 0,
    "speed": 0,
    "health": 10,
    "action": 0})

BASE_ITEMS["legs"] = Item(
    "leather leggings",
    "legs",
    {"attack": 0,
    "defense": 1,
    "magic": 0,
    "resist": 0,
    "speed": 0,
    "health": 5,
    "action": 0})

BASE_ITEMS["feet"] = Item(
    "leather boots",
    "feet",
    {"attack": 0,
    "defense": 1,
    "magic": 0,
    "resist": 0,
    "speed": 0,
    "health": 0,
    "action": 0})

# Magic Segment
ITEMS["wizard's wand"] = Item(
    "wizard's wand",
    "hand",
    {"attack": 0,
    "defense": 0,
    "magic": 3,
    "resist": 0,
    "speed": 0,
    "health": 0,
    "action": 0})

ITEMS["cloth head"] = Item(
    "cloth hood",
    "head",
    {"attack": 0,
    "defense": 1,
    "magic": 1,
    "resist": 1,
    "speed": 0,
    "health": 0,
    "action": 0})


ITEMS["cloth robes"] = Item(
    "cloth robes",
    "body",
    {"attack": 0,
    "defense": 1,
    "magic": 1,
    "resist": 1,
    "speed": 0,
    "health": 10,
    "action": 0})

ITEMS["cloth leggings"] = Item(
    "cloth leggings",
    "legs",
    {"attack": 0,
    "defense": 1,
    "magic": 1,
    "resist": 1,
    "speed": 0,
    "health": 5,
    "action": 0})

ITEMS["crocs 'n socks"] = Item(
    "crocs 'n socks",
    "feet",
    {"attack": 0,
    "defense": 1,
    "magic": 1,
    "resist": 1,
    "speed": 0,
    "health": 0,
    "action": 0})

# Light Armor Segment
ITEMS["short sword"] = Item(
    "short sword",
    "hand",
    {"attack": 2,
    "defense": 0,
    "magic": 0,
    "resist": 0,
    "speed": 1,
    "health": 0,
    "action": 0})

ITEMS["reinforced cap"] = Item(
    "reinforced cap",
    "head",
    {"attack": 0,
    "defense": 2,
    "magic": 0,
    "resist": 1,
    "speed": 0,
    "health": 0,
    "action": 0})

ITEMS["reinforced chestpiece"] = Item(
    "reinforced chestpiece",
    "body",
    {"attack": 0,
    "defense": 2,
    "magic": 0,
    "resist": 1,
    "speed": 0,
    "health": 15,
    "action": 0})

ITEMS["reinforced leggings"] = Item(
    "reinforced leggings",
    "legs",
    {"attack": 0,
    "defense": 2,
    "magic": 0,
    "resist": 1,
    "speed": 0,
    "health": 10,
    "action": 0})

ITEMS["reinforced boots"] = Item(
    "reinforced boots",
    "feet",
    {"attack": 0,
    "defense": 2,
    "magic": 0,
    "resist": 1,
    "speed": 0,
    "health": 0,
    "action": 0})

# Heavy Armor Segment
ITEMS["iron shield"] = Item(
    "iron shield",
    "hand",
    {"attack": 0,
    "defense": 4,
    "magic": 0,
    "resist": 2,
    "speed": 0,
    "health": 0,
    "action": 5})

ITEMS["heavy mace"] = Item(
    "heavy mace",
    "hand",
    {"attack": 5,
    "defense": 0,
    "magic": 0,
    "resist": 0,
    "speed": 0,
    "health": 0,
    "action": 5})

ITEMS["iron helmet"] = Item(
    "iron helmet",
    "head",
    {"attack": 0,
    "defense": 3,
    "magic": 0,
    "resist": 1,
    "speed": 0,
    "health": 0,
    "action": 2.5})


ITEMS["iron plating"] = Item(
    "iron plating",
    "body",
    {"attack": 0,
    "defense": 4,
    "magic": 0,
    "resist": 2,
    "speed": 0,
    "health": 20,
    "action": 10})

ITEMS["iron leggings"] = Item(
    "iron leggings",
    "legs",
    {"attack": 0,
    "defense": 4,
    "magic": 0,
    "resist": 2,
    "speed": 0,
    "health": 10,
    "action": 10})

ITEMS["iron boots"] = Item(
    "iron boots",
    "feet",
    {"attack": 0,
    "defense": 3,
    "magic": 0,
    "resist": 0,
    "speed": 1,
    "health": 0,
    "action": 2.5})

# EXTRA SEGMENT
ITEMS["copper ring"] = Item(
    "iron boots",
    "extra",
    {"attack": 0,
    "defense": 0,
    "magic": 0,
    "resist": 0,
    "speed": 0,
    "health": 0,
    "action": 0})