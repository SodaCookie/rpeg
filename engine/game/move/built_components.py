"""Compilation of the components to be combined to create moves"""

from engine.game.move.component import Component
import engine.game.player.player as Player
import random

class SingleTarget(Component):
    """Defines Single Targetting for a move"""
    def get_targets(self, selected, caster, players, monsters):
        return selected

class GroupTarget(Component):
    """Defines Group Targetting for a move"""
    def get_targets(self, selected, caster, players, monsters):
        if isinstance(selected[0], Player):
            return players
        return monsters

class RandomAllyTarget(Component):
    """Defines Random Ally Target for a move"""
    def get_targets(self, selected, caster, players, monsters):
        if isinstance(Player, type(caster)):
            return [random.choice([player for player in players if \
                not player.fallen])]
        return [random.choice([monster for monster in monsters if \
            not monster.fallen])]

class RandomEnemyTarget(Component):
    """Defines Random Enemy Target for a move"""
    def get_targets(self, selected, caster, players, monsters):
        if not isinstance(Player, type(caster)):
            return [random.choice([player for player in players if \
                not player.fallen])]
        return [random.choice([monster for monster in monsters if \
            not monster.fallen])]

class TargetNumberOnly(Component):
    """Descriptor for targetting a specific number of characters only"""
    def __init__(self, number):
        self.number = number

    def valid_targets(self, selected, caster, players, monsters):
        return len(selected) == self.number

class TargetOneOnly(TargetNumberOnly):
    """Descriptor for targetting one character only"""
    def __init__(self):
        super().__init__(1)

class AlliesOnly(Component):
    """Descriptor for targetting allies only"""
    def valid_targets(self, selected, caster, players, monsters):
        return all([isinstance(t, type(caster)) for t in selected])

class EnemiesOnly(Component):
    """Descriptor for targetting enemies only"""
    def valid_targets(self, selected, caster, players, monsters):
        return all([not isinstance(t, type(caster)) for t in selected])

class AddEffect(Component):
    """Applies an effect of target(s)"""
    def __init__(self, effect):
        self.effect = effect

    def on_cast(self, target, caster, players, monsters):
        damage = target.add_effect(self.effect)
        return ""

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
            damage = mod.modify(damage, target, caster, players, monsters)
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
        for mod in modifiers:
            heal = modify(heal, target, caster, players, monsters)
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
    """Component that will execute component 1 if given condition is
    True else will execute component 2"""
    def __init__(self, condition, component1, component2):
        self.condition = condition
        self.component1 = component1
        self.component2 = component2

    def on_cast(self, target, caster, players, monsters):
        if self.condition(target, caster, players, monsters):
            return self.component1.on_cast(target, caster, players, monsters)
        return self.component2.on_cast(target, caster, players, monsters)

class Message(Component):
    """Component that will return a message"""
    def __init__(self, message):
        self.message = message

    def on_cast(self, target, caster, players, monsters):
        return self.message