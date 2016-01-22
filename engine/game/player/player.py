from collections import OrderedDict
from engine.game.move.built_moves import SKILL_TREE, PLAYER_MOVES
from random import choice, sample

import engine.game.character.character as character

class Player(character.Character):
    """The friendly characters encountered in.out of battle. The Player object
    is responsible for holding a Players's stats as well as handling equipment,
    experience and level"""

    MAX_LEVEL = 15
    POINTS_PER_LEVEL = 10
    FEMALE_PORTRAITS = ["image/player/female1.png",
                        "image/player/female2.png",
                        "image/player/female3.png",
                        "image/player/female4.png"]
    MALE_PORTRAITS = ["image/player/male1.png",
                      "image/player/male2.png",
                      "image/player/male3.png",
                      "image/player/male4.png"]

    def __init__(self, name, race="human"):
        super().__init__(name)
        self.skill_points = 0
        self.experience = 0
        self.level = 1
        self.race = race
        self.gender = choice(["male", "female"])
        self.castbar = [None for i in range(10)]
        self.equipment = OrderedDict()
        self.equipment["hand1"] = None
        self.equipment["hand2"] = None
        self.equipment["body"] = None
        self.equipment["legs"] = None
        self.equipment["feet"] = None
        self.equipment["head"] = None
        self.equipment["extra1"] = None
        self.equipment["extra2"] = None
        self.inventory = [None, None, None, None]
        self.level_up_moves = None
        if self.gender == "male":
            self.portrait = choice(Player.MALE_PORTRAITS)
        else:
            self.portrait = choice(Player.FEMALE_PORTRAITS)

    def equip(self, item, slot):
        """Try to equip item into the slot"""
        if self.equipment.get(slot) == None:
            return False

        self.equipment[slot] = item
        # Update new attributes?
        return True

    def get_stat(self, stat_type):
        """Can be only used for health, attack, defense, speed,
        resist, magic takes into account"""
        stat = self.stats[stat_type]
        for item in self.equipment.values():
            if item:
                stat += item.stats[stat_type]
        for effect in self.effects:
            if not effect.active:
                continue
            stat = effect.on_get_stat(stat, stat_type)
        return int(stat)

    def remove_item(self, name):
        """Returns True is item is removed"""
        for key, item in self.equipment.items():
            if item != None:
                if item.name == name:
                    player.equip(None, key)
                    return True
        for item in self.inventory:
            if item != None:
                if item.name == name:
                    player.equip(None, key)
                    return True
        return False

    def give_experience(self, experience):
        """Grants experience to a player"""
        if self.level < Player.MAX_LEVEL:
            if self.level*100+experience > Player.MAX_LEVEL*100:
                experience = (self.level*100+experience)-Player.MAX_LEVEL*100
            self.experience += experience
        return experience

    def get_level(self):
        return self.level

    def roll_moves(self):
        """Rolls moves"""
        if self.level_up_moves:
            return # Do not regenerate

        available_moves = set()
        current_moves = set(move.name for move in self.moves)

        for name in current_moves:
            available_moves = available_moves.union(set(SKILL_TREE[name]))
        available_moves.difference_update(current_moves)
        if len(available_moves) >= 3:
            move_names = sample(available_moves, 3)
        else:
            move_names = sample(available_moves, len(available_moves))
        self.level_up_moves = [PLAYER_MOVES[name] for name in move_names]

    def can_level_up(self, shards):
        """Returns if the party has enough shards to level up"""
        return shards >= self.level * 10

    def level_up(self, move):
        """Increases the stats of a character."""
        increase_stats = {
            "attack" : 2,
            "magic" : 2,
            "defense" : 2,
            "resist" : 2,
            "health" : 10,
            "speed" : 2,
            "action" : 0
        }

        # Compile stat dist
        for stype, value in move.statdist.items():
            increase_stats[stype] += value

        # Increase base stats of character
        for stype, value in increase_stats.items():
            self.stats[stype] += value

        # Add move to the player
        self.add_move(move)
        self.level += 1
        self.full_heal()

    def get_equip(self, slot):
        return self.equipment[slot]