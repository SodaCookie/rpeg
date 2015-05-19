import item
import pickle
import math
import random

class Character(object):

    DAMAGE_VARIATION = 20
    HEAL_VARIATION = 20

    def __init__(self, name):
        self.name = name
        self.effects = []
        self.moves = []
        self.fallen = False
        self.drop = None
        self.args = []
        self.skill_points = 0

        self.attack = 10
        self.defense = 0
        self.magic = 5
        self.current_health = 100
        self.health = 100
        self.resist = 0
        self.speed = 5

        self.base_attack = 10
        self.base_defense = 0
        self.base_magic = 5
        self.base_health = 100
        self.base_speed = 5
        self.base_resist = 0

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

    def handle(self, battle):
        self.next_move.cast(battle)

        # Remove the effect after the duration is gone
        for effect in self.effects[:]:
            effect.duration -= 1
            if effect.duration <= 0:
                self.effects.remove(effect)

    def deal_damage(self, battle, source, damage, damage_type):
        for effect in self.effects:
            damage = effect.on_damage(battle, source, damage, damage_type)
        damage = int(damage - self.get_defense() * (random.randint(100-Character.DAMAGE_VARIATION, 100+Character.DAMAGE_VARIATION)/100))
        if damage <= 0:
            damage = 1
        self.current_health -= damage
        return damage

    def apply_heal(self, battle, source, heal):
        for effect in self.effects:
            if not effect.active:
                continue
            heal = effect.on_heal(battle, source, heal)
        heal = round(heal)
        heal = int(heal*(random.randint(100-Character.HEAL_VARIATION, 100+CharacterHEAL_VARIATION)/100))
        if self.fallen:
            heal = 0
        if self.current_health + heal > self.health:
            self.current_health = self.health
        else:
            self.current_health += heal
        return heal

    def get_attack(self):
        attack = self.attack
        for effect in self.effects:
            if not effect.active:
                continue
            attack = effect.on_get_stat(attack, "attack")
        return int(attack)

    def get_defense(self):
        defense = self.defense
        for effect in self.effects:
            if not effect.active:
                continue
            defense = effect.on_get_stat(defense, "defense")
        return int(defense)

    def get_speed(self):
        speed = self.speed
        for effect in self.effects:
            if not effect.active:
                continue
            speed = effect.on_get_stat(speed, "speed")
        return int(speed)

    def get_resist(self):
        resist = self.resist
        for effect in self.effects:
            if not effect.active:
                continue
            resist = effect.on_get_stat(resist, "resist")
        return int(resist)

    def get_magic(self):
        magic = self.magic
        for effect in self.effects:
            if not effect.active:
                continue
            magic = effect.on_get_stat(magic, "magic")
        return int(magic)

    def get_cur_health(self):
        return self.current_health()

    def get_max_health(self):
        health = self.health
        for effect in self.effects:
            if not effect.active:
                continue
            health = effect.on_get_stat(health, "health")
        return int(health)

    def add_effect(self, effect):
        for eff in self.effects:
            if eff.name == effect.name:
                eff.duration = effect.duration
                return
        self.effects.append(effect)

    def remove_effect(self, ename):
        for eff in self.effects[:]:
            if eff.name == ename:
                self.effects.remove(eff)
                return True
        return False

    def remove_last_effect(self):
        if self.effects:
            self.effects = self.effects[:-1]
            return True
        return False

    def add_move(self, move):
        self.moves.append(move)
        move.set_caster(self)

    def remove_move(self, move):
        return self.moves.remove(move)