from random import choice

import objects.character as character
import objects.attribute as attribute
import objects.moves as moves
import objects.item as item

class Player(character.Character):

    MAX_LEVEL = 15
    POINTS_PER_LEVEL = 10
    FEMALE_PORTRAITS = ["images/player/female1.png",
                        "images/player/female2.png",
                        "images/player/female3.png",
                        "images/player/female4.png"]
    MALE_PORTRAITS = ["images/player/male1.png",
                      "images/player/male2.png",
                      "images/player/male3.png",
                      "images/player/male4.png"]

    def __init__(self, name, race="human"):
        super().__init__(name)
        self.skill_points = 0
        self.experience = 0
        self.level = 1
        self.target = None
        self.race = race
        self.gender = choice(["male", "female"])
        self.equipment = {}
        self.equipment["hand1"] = item.Item(0, "common", generate=False)
        self.equipment["hand2"] = item.Item(0, "common", generate=False)
        self.equipment["body"] = item.Item(0, "common", generate=False)
        self.equipment["legs"] = item.Item(0, "common", generate=False)
        self.equipment["feet"] = item.Item(0, "common", generate=False)
        self.equipment["arms"] = item.Item(0, "common", generate=False)
        self.equipment["head"] = item.Item(0, "common", generate=False)
        self.equipment["extra1"] = item.Item(0, "common", generate=False)
        self.equipment["extra2"] = item.Item(0, "common", generate=False)
        if self.gender == "male":
            self.portrait = choice(Player.MALE_PORTRAITS)
        else:
            self.portrait = choice(Player.FEMALE_PORTRAITS)

    def update(self):
        self.attack = self.base_attack
        self.defense = self.base_defense
        self.health = self.base_health
        self.speed = self.base_speed
        self.magic = self.base_magic
        self.resist = self.base_resist
        for item in self.equipment.values():
            self.attack += item.attack
            self.defense += item.defense
            self.health += item.health
            self.speed += item.speed
            self.magic += item.magic
            self.resist += item.resist

    def config_for_new_battle(self):
        self.update()

    def equip(self, item, slot=""):
        """Try to equip item into the slot"""
        if not slot: slot = item.slot
        if self.equipment.get(slot) == None:
            return False
        if item.slot not in slot:
            return False
        self.equipment[slot] = item
        self.update()
        return True

    def give_experience(self, experience):
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