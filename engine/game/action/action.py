"""Defines the actions"""

import random
from engine.game.monster.monster import Monster


def action_nothing(game, **kwargs):
    """Does nothing"""
    pass

def action_battle(game, **kwargs):
    """Implements a battle"""
    defaults = {
        "challenge" : random.randint(3, 7), # TO FIX
        "monsters" : None
    }
    defaults.update(kwargs)
    if defaults["monsters"] == None:
        names = []
        while defaults["challenge"] > 0 and len(names) < 3:
            valid_monsters = [(name, monster["rating"])
                for name, monster in Monster.MONSTERS.items()
                if monster["rating"] <= defaults["challenge"] and \
                monster["location"] == game.floor_type and \
                not monster["unique"]]
            if not valid_monsters:
                break #failsafe
            name, rating = random.choice(valid_monsters)
            names.append(name)
            defaults["challenge"] -= rating
        if defaults["challenge"]: # Any rating left over
                                  # then we add the highest
            valid_monsters = [(name, monster["rating"])
                for name, monster in Monster.MONSTERS.items()
                if monster["rating"] <= defaults["challenge"] and \
                monster["location"] == game.floor_type and \
                not monster["unique"]]

            highest_value = 0
            for name, value in valid_monsters:
                if value > highest_value:
                    highest_value = value
            valid_names = [name for name, value in valid_monsters
                           if value <= highest_value]
            names.append(random.choice(valid_names))
        defaults["monsters"] = [Monster(name) for name in names]
    else:
        names = defaults["monsters"].split(',')
        defaults["monsters"] = [Monster(name.replace("_", " ")) \
            for name in names]
    monsters = defaults["monsters"]
    game.encounter = defaults["monsters"]

def action_loot(game, **kwargs):
    """Gives party loot"""
    defaults = {
        "reward-tier" : "low",
        "shard" : None,
        "item" : None
    }
    defaults.update(kwargs)
    # Handle unspecified shard
    if defaults["shard"] == None: # arbitrary
        if defaults["reward-tier"] == "low":
            defaults["shard"] = game.floor_level * random.randint(15, 20)
        elif defaults["reward-tier"] == "medium":
            defaults["shard"] = game.floor_level * random.randint(30, 35)
        elif defaults["reward-tier"] == "high":
            defaults["shard"] = game.floor_level * random.randint(50, 70)
    else:
        defaults["shard"] = int(defaults["shard"])
    # Handle unspecified item
    if defaults["item"] == None:
        defaults["item"] = []
        parameters = {
            "floor": game.floor_level,
            "floor-type": game.floor_type
        }
        if "reward-tier" == "medium":
            if random.randint(0, 99) < 50:
                defaults.append(Item(**parameters))
        elif "reward-tier" == "high":
            game.floor_level * random.randint(50, 70)
            if random.randint(0, 99) < 30:
                defaults.append(Item(**parameters))
    # Handle raw input as a string for item
    else:
        # item := <name>,<parameter>|[<more parameters>]@[<item>]
        items = defaults["item"]
        defaults["item"] = []
        if items:
            for item_parameters in items.split("@"):
                # to be fed into the builders
                parameters = {
                    "floor": game.floor_level,
                    "floor-type": game.floor_type
                }
                for parameter in item_parameters.split("|"):
                    parameter_name = parameter.split(",")[0]
                    parameter_value = parameter.split(",")[1]
                    parameters[parameter_name] = parameter_value
                defaults["item"].append(Item(**parameters))
    game.loot = (defaults["shard"], defaults["item"])
    game.party.shards += defaults["shard"]
    game.focus_window = "loot"

ACTIONS = {
    "" : action_nothing,
    "battle" : action_battle,
    "loot" : action_loot
}