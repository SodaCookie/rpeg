"""Defines the actions"""

import random
import re

from engine.game.monster.monster import Monster
from engine.game.effect.built_scenario_effect import SCENARIO_EFFECTS

from engine.game.item.item_factory import ItemFactory


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
        if "reward-tier" == "medium":
            # 50% change of getting an item of "medium" reward tier
            # Additionally, "medium" tier can only generate "rare"(s)
            if random.randint(0, 99) < 50:
                defaults.append(ItemFactory.generate(
                    game.encounter,
                    game.floor_type,
                    rarity="rare"))
        elif "reward-tier" == "high":
            # 70% change of getting an item of "high" reward tier
            if random.randint(0, 99) < 70:
                defaults["item"].append(ItemFactory.generate(
                    game.encounter,
                    game.floor_type))
    # Handle raw input as a string for item
    else:
        # item := <name>,[...]
        items = defaults["item"]
        defaults["item"] = []
        # Find item in list in premade items
        for item_name in items.split(","):
            defaults["item"].append(ItemFactory.static_generate(
                item_name))
    game.loot = (defaults["shard"], defaults["item"])
    game.party.add_shards(defaults["shard"])
    game.focus_window = "loot"

def action_add_action(game, **kwargs):
    """Action to add actions"""
    defaults = {
        "target" : "all", # Values can be all, random, or random number
        "percent" : "100" # Values from 1-100, percent to charge
    }
    defaults.update(kwargs)
    percent = int(defaults["percent"])
    if defaults["target"] == "all":
        for player in game.party.players:
            player.build_action(percent/100*player.get_stat("action"))
    elif defaults["target"] == "random":
        player = random.choice(game.party.players)
        player.build_action(percent/100*player.get_stat("action"))
    elif re.match(r"^random\d+", defaults["target"]):
        num_targets = int(defaults["target"].replace("random", ""))
        for player in random.sample(game.party.players, num_targets):
            player.build_action(percent/100*player.get_stat("action"))
    else:
        # Logging?
        print("Target has an incorrect argument")

def action_remove_shard(game, **kwargs):
    """Action to remove a shard. Proper use requires if the party has
    enough shard. If amount is over than party shard amount is 0"""
    defaults = {
        "shard" : 0, # amount to remove
    }
    defaults.update(kwargs)
    if re.match(r"^\d+", kwargs["shard"]):
        game.party.remove_shards(int(kwargs["shard"]))
    else:
        print("Shard has an incorrect argument")

def action_apply_effect(game, **kwargs):
    defaults = {
        "target" : "all", # Values can be all, random, or random number
        "effect" : None
    }
    defaults.update(kwargs)
    if defaults["target"] == "all":
        for player in game.party.players:
            player.add_effect(SCENARIO_EFFECTS[defaults["effect"]])
    elif defaults["target"] == "random":
        player = random.choice(game.party.players)
        player.add_effect(SCENARIO_EFFECTS[defaults["effect"]])
    elif re.match(r"^random\d+", defaults["target"]):
        num_targets = int(defaults["target"].replace("random", ""))
        for player in random.sample(game.party.players, num_targets):
            player.add_effect(SCENARIO_EFFECTS[defaults["effect"]])
    else:
        # Logging?
        print("Target has an incorrect argument")

def action_apply_attribute(game, **kwargs):
    defaults = {
        "target" : "all", # Values can be all, random, or random number
        "effect" : None
    }
    defaults.update(kwargs)
    if defaults["target"] == "all":
        for player in game.party.players:
            player.add_effect(SCENARIO_ATTRIBUTES[defaults["effect"]])
    elif defaults["target"] == "random":
        player = random.choice(game.party.players)
        player.add_effect(SCENARIO_ATTRIBUTES[defaults["effect"]])
    elif re.match(r"^random\d+", defaults["target"]):
        num_targets = int(defaults["target"].replace("random", ""))
        for player in random.sample(game.party.players, num_targets):
            player.add_effect(SCENARIO_ATTRIBUTES[defaults["effect"]])
    else:
        # Logging?
        print("Target has an incorrect argument")

def action_remove_item(game, **kwargs):
    """Needs to be called with has item condition"""
    defaults = {
        "item" : None
    }
    defaults.update(kwargs)
    for player in game.party.players:
        if player.remove_item(defaults["name"]):
            break


def action_kill(game, **kwargs):
    """Action to kill"""
    defaults = {
        "target" : "all", # Values can be all, random, or random number
    }
    defaults.update(kwargs)
    if defaults["target"] == "all":
        for player in game.party.players:
            player.kill()
    elif defaults["target"] == "random":
        player = random.choice(game.party.players)
        player.kill()
    elif re.match(r"^random\d+", defaults["target"]):
        num_targets = int(defaults["target"].replace("random", ""))
        for player in random.sample(game.party.players, num_targets):
            player.kill()
    else:
        # Logging?
        print("Target has an incorrect argument")

def action_revive(game, **kwargs):
    """Action to revive"""
    defaults = {
        "target" : "all", # Values can be all, random, or random number
    }
    defaults.update(kwargs)
    if defaults["target"] == "all":
        for player in game.party.players:
            player.revive()
    elif defaults["target"] == "random":
        player = random.choice(game.party.players)
        player.revive()
    elif re.match(r"^random\d+", defaults["target"]):
        num_targets = int(defaults["target"].replace("random", ""))
        for player in random.sample(game.party.players, num_targets):
            player.revive()
    else:
        # Logging?
        print("Target has an incorrect argument")

def action_full_restore(game, **kwargs):
    """Action to full restore"""
    defaults = {
        "target" : "all", # Values can be all, random, or random number
    }
    defaults.update(kwargs)
    if defaults["target"] == "all":
        for player in game.party.players:
            player.full_heal()
    elif defaults["target"] == "random":
        player = random.choice(game.party.players)
        player.full_heal()
    elif re.match(r"^random\d+", defaults["target"]):
        num_targets = int(defaults["target"].replace("random", ""))
        for player in random.sample(game.party.players, num_targets):
            player.full_heal()
    else:
        # Logging?
        print("Target has an incorrect argument")

def action_cleanse(game, **kwargs):
    """Action to cleanse"""
    defaults = {
        "target" : "all", # Values can be all, random, or random number
    }
    defaults.update(kwargs)
    if defaults["target"] == "all":
        for player in game.party.players:
            player.cleanse()
    elif defaults["target"] == "random":
        player = random.choice(game.party.players)
        player.cleanse()
    elif re.match(r"^random\d+", defaults["target"]):
        num_targets = int(defaults["target"].replace("random", ""))
        for player in random.sample(game.party.players, num_targets):
            player.cleanse()
    else:
        # Logging?
        print("Target has an incorrect argument")


ACTIONS = {
    "" : action_nothing,
    "battle" : action_battle,
    "loot" : action_loot,
    "action-full-restore" : action_full_restore,
    "remove-shard" : action_remove_shard,
    "remove-item" : action_remove_item,
    "apply-effect" : action_apply_effect,
    "apply-attribute" : action_apply_attribute,
    "kill" : action_kill,
    "revive" : action_revive,
    "full_restore" : action_full_restore,
    "cleanse" : action_cleanse
}