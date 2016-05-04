from engine.game.attribute import RARE_ATTRIBUTES, LEGENDARY_ATTRIBUTES,UNIQUE_ATTRIBUTES

def create(name, quality):
    if(quality == "rare"):
        RARE_ATTRIBUTES[name] = None
    elif(quality == "legendary"):
        LEGENDARY_ATTRIBUTES[name] = None
    elif(quality == "unique"):
        UNIQUE_ATTRIBUTES[name] = None

def set_name(old_name, new_name, quality):
    if(quality == "rare"):
        RARE_ATTRIBUTES[new_name] = RARE_ATTRIBUTES[old_name]
        del RARE_ATTRIBUTES[old_name]
    elif(quality == "legendary"):
        LEGENDARY_ATTRIBUTES[new_name] = LEGENDARY_ATTRIBUTES[old_name]
        del LEGENDARY_ATTRIBUTES[old_name]
    elif(quality == "unique"):
        UNIQUE_ATTRIBUTES[new_name] = UNIQUE_ATTRIBUTES[old_name]
        del UNIQUE_ATTRIBUTES[old_name]

def update(name, quality, attribute):
    if(quality == "rare"):
        RARE_ATTRIBUTES[name].update(attribute)
    elif(quality == "legendary"):
        LEGENDARY_ATTRIBUTES[name].update(attribute)
    elif(quality == "unique"):
        UNIQUE_ATTRIBUTES[name].update(attribute)

def delete(name, quality):
    if(quality == "rare"):
        del RARE_ATTRIBUTES[name]
    elif(quality == "legendary"):
        del LEGENDARY_ATTRIBUTES[name]
    elif(quality == "unique"):
        del UNIQUE_ATTRIBUTES[name]