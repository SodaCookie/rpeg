from engine.game.move.component import Component
# from engine.game.monster.monster import Monster
# from engine.game.player.player import Player

# Temp
class Character: pass
class Monster(Character): pass
class Player(Character): pass

class SingleTarget(Component):
    """Defines Single Targetting for a move"""
    def get_targets(self, selected, caster, players, monsters):
        return [selected]

class GroupTarget(Component):
    """Defines Group Targetting for a move"""
    def get_targets(self, selected, caster, players, monsters):
        if isinstance(selected, Monster):
            return monsters
        return players

class AlliesOnly(Component):
    """Descriptor for targetting allies only"""
    def valid_targets(self, selected, caster, players, monsters, targets):
        return all([isinstance(caster, t) for t in targets])

class EnemiesOnly(Component):
    """Descriptor for targetting enemies only"""
    def valid_targets(self, selected, caster, players, monsters, targets):
        return all([not isinstance(caster, t) for t in targets])

class Effect(Component):
    """Applies an effect of target(s)"""
    def __init__(self, effect):
        self.effect = effect

    def on_cast(self, target, caster, players, monsters):
        damage = target.add_effect(self.effect)
        return ""

class Damage(Component):
    """Deals flat damage to given targets"""
    def __init__(self, damage, dtype):
        self.damage = damage
        self.dtype = dtype

    def on_cast(self, target, caster, players, monsters):
        damage = target.deal_damage(caster, self.damage, self.dtype)
        return "%s dealt %d %s damage to %s" % \
            (caster.name, damage, self.dtype, target.name)

class ScaleDamage(Damage):
    """Deals scaling damage to given targets"""
    def __init__(self, damage, dtype, scaling, stype):
        super().__init__(damage, dtype)
        self.scaling = scaling
        self.stype = stype

    def on_cast(self, target, caster, players, monsters):
        if self.stype == "attack":
            scale = caster.get_attack()
        elif self.stype == "defense":
            scale = caster.get_defense()
        elif self.stype == "health":
            scale = caster.get_max_defense()
        elif self.stype == "magic":
            scale = caster.get_magic()
        elif self.stype == "resist":
            scale = caster.get_resist()
        elif self.stype == "speed":
            scale = caster.get_speed()
        scaled_damage = self.damage + self.scaling * scale
        damage = target.deal_damage(caster, scaled_damage, self.dtype)
        return "%s dealt %d %s damage to %s" % \
            (caster.name, damage, self.dtype, target.name)

class Heal(Component):
    """Deals flat healing to given targets"""
    def __init__(self, heal):
        self.heal = heal

    def on_cast(self, target, caster, players, monsters):
        heal = target.apply_heal(caster, self.heal)
        return "%s healed %s for %d health" % \
            (caster.name, target.name, heal)

class ScaleHeal(Heal):
    """Deals scaling healing to given targets"""
    def __init__(self, heal, scaling, stype):
        super().__init__(heal)
        self.scaling = scaling
        self.stype = stype

    def on_cast(self, target, caster, players, monsters):
        if self.stype == "attack":
            scale = caster.get_attack()
        elif self.stype == "defense":
            scale = caster.get_defense()
        elif self.stype == "health":
            scale = caster.get_max_defense()
        elif self.stype == "magic":
            scale = caster.get_magic()
        elif self.stype == "resist":
            scale = caster.get_resist()
        elif self.stype == "speed":
            scale = caster.get_speed()
        scaled_heal = self.heal + self.scaling * scale
        heal = target.apply_heal(caster, scaled_heal)
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