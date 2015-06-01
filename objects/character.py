import objects.item as item
import pickle
import math
import random

from controller import BattleController

class Character(BattleController):

    ACTION_SPEED = 25 # how quickly the action bar goes up
    SPEED_CAP = 5 # times the normal speed
    SPEED_BASE = 50 # diminishing returns shows how fast speed will go
    DAMAGE_VARIATION = 20
    HEAL_VARIATION = 20

    def __init__(self, name):
        super().__init__()

        self.name = name
        self.effects = []
        self.moves = []
        self.fallen = False
        self.drop = None
        self.args = []
        self.overflow = 0

        self.attack = 10
        self.defense = 0
        self.magic = 5
        self.current_health = 100
        self.health = 100
        self.resist = 0
         # enough to do 1 ACTION_SPEED per second
        self.speed = Character.SPEED_BASE/(Character.SPEED_CAP-1)
        self.action_max = 100
        self.action = 0
        self.ready = False

        self.base_attack = 10
        self.base_defense = 0
        self.base_magic = 5
        self.base_health = 100
        self.base_speed = 5
        self.base_resist = 0

    def battle(self, delta):

        steps = math.floor(self.overflow+delta)        # Used for buffs/debuffs
        self.overflow = (self.overflow+delta)-steps    # Used for carry over
        self.decrease_durations(steps)
        action = delta * Character.ACTION_SPEED *\
            (Character.SPEED_CAP*self.speed/(Character.SPEED_BASE+self.speed))
        if action == 0: # being nice as if you have speed 1
            action = delta * Character.ACTION_SPEED *\
                (Character.SPEED_CAP*1/\
                (Character.SPEED_BASE+1))
        self.build_action(action)
        if self.action == self.action_max and not self.ready:
            # Available to cast
            self.start_turn()
        if self.action < self.action_max:
            self.ready = False

    def cast(self, move, battle):
        if move in self.moves:
            move.cast(battle)
        self.action = 0

    def start_turn(self):
        for effect in self.effects:
            effect.on_start_turn()
        self.ready = True

    def decrease_durations(self, amount):
        for effect in self.effects:
            if effect.duration == "permanent":
                continue
            effect.duration -= amount
        self.effects = filter(lambda effect: effect.duration == "permanent"
                              or effect.duration > 0, self.effects)
        removed = filter(lambda effect: not effect.active
                                      or effect.duration <= 0, self.effects)
        for effect in removed:
            effect.on_remove()

    def build_action(self, action):
        for effect in self.effects:
            action = effect.on_build_action(action)
        self.action += action
        if self.action < 0:
            self.action = 0
        elif self.action > self.action_max:
            self.action = self.action_max

    def deal_damage(self, source, damage, damage_type):
        for effect in self.effects:
            damage = effect.on_damage(source, damage, damage_type)
        damage = int(damage - self.get_defense() * (random.randint(100-Character.DAMAGE_VARIATION, 100+Character.DAMAGE_VARIATION)/100))
        if damage <= 0:
            damage = 1
        for effect in source.effects:
            damage = effect.on_deal_damage()
        self.current_health -= damage
        return damage

    def apply_heal(self, source, heal):
        for effect in self.effects:
            if not effect.active:
                continue
            heal = effect.on_heal(battle, source, heal)
        heal = round(heal)
        heal = int(heal*(random.randint(100-Character.HEAL_VARIATION, 100+CharacterHEAL_VARIATION)/100))
        if self.fallen:
            heal = 0
        for effect in source.effects:
            heal = effect.on_apply_heal(heal)
        if self.current_health + heal > self.get_max_health():
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
                eff.on_refresh(effect)
                return
        effet.set_owner(self)
        self.effects.append(effect)

    def remove_effect(self, ename):
        for eff in self.effects[:]:
            if eff.name == ename and eff.duration != "permanent":
                self.effects.remove(eff)
                return True
        return False

    def add_move(self, move):
        self.moves.append(move)
        move.set_caster(self)

    def remove_move(self, move):
        return self.moves.remove(move)