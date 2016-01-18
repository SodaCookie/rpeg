from collections import OrderedDict
from random import choice

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

    def is_level_up(self):
        if self.experience >= 100:
            return True
        return False

    def level_up(self):
        """Increases the stats of a character."""
        counter = 0
        gain_attack = 0
        gain_defense = 0
        gain_health = 0
        gain_speed = 0
        gain_magic = 0
        gain_resist = 0

        attack = 1
        defense = 1
        health = 1
        speed = 1
        magic = 1
        resist = 1

        while self.experience >= 100:
            self.experience -= 100
            self.level += 1
            self.skill_points += 1
            counter += 1

            for item in self.equipment.values():
                attack += item.attack
                defense += item.defense
                health += item.health
                speed += item.speed
                magic += item.magic
                resist += item.resist

            total = attack + defense + health + speed + magic + resist
            attack_weight = attack/total
            defense_weight = defense/total
            health_weight = health/total
            speed_weight = speed/total
            magic_weight = magic/total
            resist_weight = resist/total

            gain_attack += round(attack_weight * Player.POINTS_PER_LEVEL)
            gain_defense += round(defense_weight * Player.POINTS_PER_LEVEL)
            gain_health += round(health_weight * Player.POINTS_PER_LEVEL)
            gain_speed += round(speed_weight * Player.POINTS_PER_LEVEL)
            gain_magic += round(magic_weight * Player.POINTS_PER_LEVEL)
            gain_resist += round(resist_weight * Player.POINTS_PER_LEVEL)

        self.base_attack += gain_attack
        self.base_defense += gain_defense
        self.base_health += gain_health
        self.base_speed += gain_speed
        self.base_magic += gain_magic
        self.base_resist += gain_resist

    def get_equip(self, slot):
        return self.equipment[slot]