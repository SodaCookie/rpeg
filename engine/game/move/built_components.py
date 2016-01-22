"""Compilation of the components to be combined to create moves"""

from engine.game.move.component import Component
import random

class SelfCast(Component):
    """Targeting scheme for self only"""
    def get_targets(self, selected, caster, players, monsters):
        return [caster]

class SingleCast(Component):
    """Defines Single Targetting for a move"""
    def get_targets(self, selected, caster, players, monsters):
        return selected

class GroupCast(Component):
    """Defines Group Targetting for a move"""
    def get_targets(self, selected, caster, players, monsters):
        if isinstance(selected[0], type(players[0])):
            return players
        return monsters

class EnemiesCast(Component):
    """Defines Enemy Targetting for a move"""
    def get_targets(self, selected, caster, players, monsters):
        if isinstance(caster, type(players[0])):
            return monsters
        return players

class AlliesCast(Component):
    """Defines Ally Targetting for a move"""
    def get_targets(self, selected, caster, players, monsters):
        if isinstance(caster, type(players[0])):
            return players
        return monsters

class RandomAllyCast(Component):
    """Defines Random Ally Target for a move"""
    def get_targets(self, selected, caster, players, monsters):
        if isinstance(type(caster), type(players[0])):
            return [random.choice([player for player in players if \
                not player.fallen])]
        return [random.choice([monster for monster in monsters if \
            not monster.fallen])]

class RandomEnemyCast(Component):
    """Defines Random Enemy Target for a move"""
    def get_targets(self, selected, caster, players, monsters):
        if not isinstance(caster, type(players[0])):
            return [random.choice([player for player in players if \
                not player.fallen])]
        return [random.choice([monster for monster in monsters if \
            not monster.fallen])]

class TargetNumberOnly(Component):
    """Descriptor for targetting a specific number of characters only"""
    def __init__(self, number):
        self.number = number

    def valid_cast(self, selected, caster, players, monsters):
        return len(selected) == self.number

    def valid_target(self, selected, caster, players, monsters):
        return len(selected) <= self.number

class TargetOneOnly(TargetNumberOnly):
    """Descriptor for targetting one character only"""
    def __init__(self):
        super().__init__(1)

class AlliesOnly(Component):
    """Descriptor for targetting allies only"""
    def valid_target(self, selected, caster, players, monsters):
        return all([isinstance(t, type(caster)) for t in selected])

class EnemiesOnly(Component):
    """Descriptor for targetting enemies only"""
    def valid_target(self, selected, caster, players, monsters):
        return all([not isinstance(t, type(caster)) for t in selected])

class AddChanceEffect(Component):
    """Chance to apply effect on target(s)"""
    def __init__(self, effect, chance):
        self.effect = effect
        self.chance = chance

    def on_cast(self, target, caster, players, monsters):
        rand = random.random()
        if rand > self.chance:
            return ""
        else:
            self.effect.set_caster(caster)
            damage = target.add_effect(self.effect)
            return ""

class AddEffect(AddChanceEffect):
    """Applies an effect of target(s)"""
    def __init__(self, effect):
        self.effect = effect
        self.chance = 1

    def on_cast(self, target, caster, players, monsters):
        self.effect.set_caster(caster)
        damage = target.add_effect(self.effect)
        return ""

class SelfEffect(Component):
    """Applies self-effect on cast"""
    def __init__(self, effect):
        self.effect = effect

    def on_cast(self, target, caster, players, monsters):
        damage = caster.add_effect(self.effect)
        return ""

class Damage(Component):
    """Deals flat damage to given targets"""
    def __init__(self, damage, dtype, modifiers=None):
        self.damage = damage
        self.dtype = dtype
        if not modifiers:
            self.modifiers = []
        else:
            self.modifiers = modifiers

    def on_cast(self, target, caster, players, monsters):
        """Order IMPORTANT in modifying damage:
        Suggested standard is additions, then multiplications"""
        damage = self.damage
        for mod in self.modifiers:
            damage = mod.modify(damage, target, caster)
        damage = target.deal_damage(caster, damage, self.dtype)
        return "%s dealt %d %s damage to %s" % \
            (caster.name, damage, self.dtype, target.name)

class ScaleMiss(Component):

    def __init__(self, scaling, stype):
        super().__init__()
        self.scaling = scaling
        self.stype = stype

    def get_miss(self, miss, selected, caster, players, monsters):
        return miss + self.scaling * caster.get_stat(self.stype)


class ScaleCrit(Component):
    #changes the critbound?

    def __init__(self, scaling, stype):
        super().__init__()
        self.scaling = scaling
        self.stype = stype

    def get_crit(self, crit, selected, caster, players, monsters):
        return crit + self.scaling * caster.get_stat(self.stype)

class Heal(Component):
    """Deals flat healing to given targets"""
    def __init__(self, heal, modifiers):
        self.heal = heal
        if not modifiers:
            self.modifiers = []
        else:
            self.modifiers = modifiers

    def on_cast(self, target, caster, players, monsters):
        """Order IMPORTANT in modifying heal:
        Suggested standard is additions, then multiplications"""
        heal = self.heal
        for mod in self.modifiers:
            heal = mod.modify(heal, target, caster)
        heal = target.apply_heal(caster, heal)
        return "%s healed %s for %d health" % \
            (caster.name, target.name, heal)

class Repeat(Component):
    """Component that will complete another component x times"""
    def __init__(self, repeat, component):
        self.repeat = repeat
        self.component = component

    def on_cast(self, target, caster, players, monsters):
        msg = ""
        for i in range(self.repeat):
            msg += self.component.on_cast(target, caster, players, monsters)+'\n'
        return msg

class Conditional(Component):
    """Component that will execute list of components 1 if given condition is
    True else will execute list of components 2"""
    def __init__(self, condition, components1, components2):
        self.condition = condition
        self.components1 = components1
        self.components2 = components2

    def on_cast(self, target, caster, players, monsters):
        msg = ""
        if self.condition(target, caster, players, monsters):
            for component in self.components1:
                msg += component.on_cast(target, caster, players, monsters)
            return msg
        else:
            for component in self.components2:
                msg += component.on_cast(target, caster, players, monsters)
            return msg

class Message(Component):
    """Component that will return a message"""
    def __init__(self, message):
        self.message = message

    def on_cast(self, target, caster, players, monsters):
        print(self.message)
        return self.message