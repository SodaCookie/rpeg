from engine.game.item.built_items import BASE_ITEMS, ITEMS

def create(name, base):
    if(base):
        BASE_ITEMS[name] = Item(
            name,
            "sword",
            {
                "health": 0,
                "attack": 0,
                "defense": 0,
                "magic": 0,
                "resist": 0,
                "speed": 0,
                "action": 0
            })
    else:
        ITEMS[name] = Item(
            name,
            "sword",
            {
                "health": 0,
                "attack": 0,
                "defense": 0,
                "magic": 0,
                "resist": 0,
                "speed": 0,
                "action": 0
            })

def set_name(old_name, new_name, base):
    if(base):
        BASE_ITEMS[new_name] = BASE_ITEMS[old_name]
        BASE_ITEMS[new_name].name = new_name
        del BASE_ITEMS[old_name]
    else:
        ITEMS[new_name] = ITEMS[old_name]
        ITEMS[new_name].name = new_name
        del ITEMS[old_name]

def update(name, base, itype, stats, slot, icon, rarity, attributes):
    if(base):
        BASE_ITEMS[name].itype = itype
        BASE_ITEMS[name].stats = stats
        BASE_ITEMS[name].slot = slot
        BASE_ITEMS[name].icon = icon
        BASE_ITEMS[name].rarity = rarity
        BASE_ITEMS[name].attributes = attributes
    else:
        ITEMS[name].itype = itype
        ITEMS[name].stats = stats
        ITEMS[name].slot = slot
        ITEMS[name].icon = icon
        ITEMS[name].rarity = rarity
        ITEMS[name].attributes = attributes

def delete(name, base):
    if(base):
        del BASE_ITEMS[name]
    else:
        del ITEMS[name]
