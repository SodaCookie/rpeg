from collections import OrderedDict
import pickle
import math
import random
import copy

from engine.game.controller.battle_controller import BattleController

class Character(BattleController):
    """Character is the base class for units that interact during battles.
    They have a collection of stats and a current status."""

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
        self.target = None
        self.args = []
        self.overflow = 0

        self.stats = OrderedDict()
        self.stats["attack"] = 10
        self.stats["defense"] = 0
        self.stats["magic"] = 10
        self.stats["health"] = 100
        self.stats["resist"] = 0
        self.current_health = self.stats["health"]
         # enough to do 1 ACTION_SPEED per second
        self.speed = Character.SPEED_BASE/(Character.SPEED_CAP-1)
        self.action_max = 100
        self.action = 0
        self.ready = False
        self.scroll = 0

    def handle_battle(self, delta):
        """Handles each characters update loop"""
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

        if self.get_cur_health() <= 0:
            if self.kill():
                self.fallen = True
            else:
                self.current_health = 1

    def is_enemy(self, character):
        if type(self) != type(character):
            return True
        return False

    def kill(self):
        """Kills this character returns True if success else False
        takes into account effects"""
        for effect in self.effects:
            if effect.active:
                if not effect.on_death():
                    return False
        self.current_health = 0
        self.fallen = True
        return True

    def hard_kill(self):
        """Kills character without taking into account effects"""
        self.current_health = 0
        self.fallen = True

    def start_turn(self):
        for effect in self.effects:
            if effect.active:
                effect.on_start_turn()
        self.ready = True

    def decrease_durations(self, amount):
        """Decreases the duration of effects by a given amount. Ignores
        permanent effects."""
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
        """Adds action to a character by the given amount. Takes into
        account effects."""
        for effect in self.effects:
            if effect.active:
                action = effect.on_build_action(action)
        self.action += action
        if self.action < 0:
            self.action = 0
        elif self.action > self.action_max:
            self.action = self.action_max

    def deal_damage(self, source, damage, damage_type):
        """Deals damage to character by the given amount. Takes into
        account effects."""
        for effect in self.effects:
            if effect.active:
                damage = effect.on_damage(source, damage, damage_type)
        damage = int(damage - self.get_stat("defense") * (random.randint(100-Character.DAMAGE_VARIATION, 100+Character.DAMAGE_VARIATION)/100))
        if damage <= 0:
            damage = 1
        for effect in source.effects:
            damage = effect.on_deal_damage()
        self.current_health -= damage
        return damage

    def apply_heal(self, source, heal):
        """Heals character by the given amount. Takes into
        account effects."""
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

    def get_stat(self, stat):
        """Can be only used for health, attack, defense, speed,
        resist, magic"""
        stat = self.stats[stat]
        for effect in self.effects:
            if not effect.active:
                continue
            stat = effect.on_get_stat(stat, stat)
        return int(stat)

    def get_cur_health(self):
        return self.current_health

    def add_effect(self, effect):
        for eff in self.effects:
            if eff.name == effect.name:
                eff.on_refresh(effect)
                return
        effet.set_owner(self)
        self.effects.append(effect)

    def remove_effect(self, ename):
        for eff in self.effects[:]:
            if eff.name == ename:
                self.effects.remove(eff)
                return True
        return False

    def add_move(self, move):
        self.moves.append(move)
        move.set_caster(self)

    def remove_move(self, move):
        return self.moves.remove(move)