from classes.game.moves import *

class SingleTarget(MoveBase):

    def get_target(self, battle):
        return [self.caster.target]

class PartyTarget(MoveBase):

    def get_target(self, battle):
        return battle.party.players

class AllEnemyTarget(MoveBase):

    def get_target(self, battle):
        return battle.monsters

class Damage(AllEnemyTarget, MoveBase):
    """Base damage class will only scale of user's attack stat.
    Implemented a basic critical (x2 damage) and damage method
    all moves extending damage should override damage"""

    def __init__(self, base, dtype, name):
        super().__init__(name)
        self.base = base
        self.dtype = dtype

    def cast(self, target):
        dmg = target.deal_damage(self.caster, self.damage(), self.dtype)

    def crit(self, target):
        dmg = target.deal_damage(self.caster, 2*self.damage(), self.dtype)

    def damage(self):
        return self.caster.get_attack()*self.base


class ScaleDamage(Damage):
    """Damage move that will scale off a different stat other than attack
    scaling is a floating point number showing the percent of the stat
    value will go into damage"""

    def __init__(self, scaling, stype, base, dtype, name):
        super().__init__(base, dtype, name)
        self.scaling = scaling
        self.stype = stype

    def damage(self):
        if self.stype == "attack":
            scale = self.caster.get_attack()
        elif self.stype == "defense":
            scale = self.caster.get_defense()
        elif self.stype == "health":
            scale = self.caster.get_max_defense()
        elif self.stype == "magic":
            scale = self.caster.get_magic()
        elif self.stype == "resist":
            scale = self.caster.get_resist()
        elif self.stype == "speed":
            scale = self.caster.get_speed()
        return scale*self.base*self.scaling

class Repeat(MoveBase):

    def __init__(self, repeat, name):
        super().__init__(name)
        self.repeat = repeat

    def cast(self, *args):
        if self.prev:
            for i in range(self.repeat):
                self.prev._cast(*args)


skill_tree = {}
skills = {}

skills["attack"] = \
    Move(80, 10, "images/icon/attack_icon.png", "enemy",
        Damage(0.5, "physical", "attack"))

skills["flurry"] = \
    Move(80, 10, "images/icon/attack_icon.png", "enemy",
        Repeat(3,
            Damage(0.3, "physical", "flurry")))

skills["magic-bolt"] = \
    Move(90, 5, "images/icon/magic_bolt_icon.png", "enemy",
        ScaleDamage(1, "magic", 0.5, "magic", "magic-bolt"))
