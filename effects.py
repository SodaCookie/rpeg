class Effect:

    def __init__(self, name, duration):
        """'name' is the identifier used to identify the effect
        duration is used to indicate how long the effect will last on the target.
        Durations for each effect on a target are decreased by 1 after that
         character's turn"""
        self.name = name
        self.duration = duration
        self.active = True

    def remove(self):
        """When called any subsequent calls to this effect will be ignored as well as removed
        useful for 1 time effects"""
        self.duration = 0
        self.active = False

    def on_get_stat(self, value, stat_type):
        """Any time a character is asked for a stat this function will be called
        and the type of stat will be used to determine how the stat will be
        affected. Returned is the stat of the player"""
        return value

    def on_start_turn(self, battle, character):
        """Return a tuple index 0 true if you can go, return false if you can't (ie stun, dead), index 1 is the message"""
        return (True, "")

    def on_damage(self, battle, source, damage, damage_type):
        return damage

    def on_heal(self, battle, source, heal):
        return heal

    def on_cast(self, battle, source, move):
        pass

    def on_death(self, battle, character):
        """If truly dead then return True"""
        return True

    def on_end_turn(self, battle, character):
        """That is the end of the characters turn (not the WHOLE turn), returns message"""
        return ""

    def __str__(self):
        return "%s - Turn(s)%d" % (self.name.replace("-", " ").title(), self.duration)


class Block(Effect):

    def __init__(self, duration, percentage, damage_type, name):
        super().__init__(name, duration)
        self.percentage = percentage
        self.damage_type = damage_type

    def on_damage(self, battle, source, damage, damage_type):
        if damage_type == self.damage_type:
            return damage*self.percentage
        return damage


class BlockAllSingle(Effect):

    def __init__(self, duration, percentage, name):
        super().__init__(name, duration)
        self.percentage = percentage

    def on_damage(self, battle, source, damage, damage_type):
        if damage_type == "true":
            return damage
        self.remove()
        return damage*self.percentage


class Slow(Effect):

    def __init__(self, duration, mod):
        super().__init__("slowed", duration)
        self.mod = mod

    def on_get_stat(self, value, stat_type):
        if stat_type == "speed":
            return value*self.mod
        return value


class Burn(Effect):

    def __init__(self, duration, caster, target, ratio):
        super().__init__("burning", duration)
        self.caster = caster
        self.damage = caster.get_magic() * ratio

    def on_end_turn(self, battle, character):
        damage = character.deal_damage(battle, self.caster, self.damage, "fire")
        return "\n" + character.name + " burned for " + str(damage) + " damage."


class Poison(Effect):

    def __init__(self, duration, caster, target, ratio):
        super().__init__("poisoned", duration)
        self.caster = caster
        self.damage = caster.get_magic() * ratio

    def on_end_turn(self, battle, character):
        damage = character.deal_damage(battle, self.caster, self.damage, "nature")
        return "\n" + character.name + " poisoned for " + str(damage) + " damage."


class Armor(Effect):

    def __init__(self, duration, mod):
        super().__init__("slowed", duration)
        self.mod = mod

    def on_get_stat(self, value, stat_type):
        if stat_type == "defense":
            return value*self.mod
        return value


class ReduceArmor(Effect):

    def __init__(self, duration, mod, name):
        super().__init__(name, duration)
        self.mod = mod

    def on_get_stat(self, value, stat_type):
        if stat_type == "defense":
            return value*self.mod
        return value

class ReduceAttack(Effect):

    def __init__(self, duration, mod, name):
        super().__init__(name, duration)
        self.mod = mod

    def on_get_stat(self, value, stat_type):
        if stat_type == "attack":
            return value*self.mod
        return value


class ReduceMagic(Effect):

    def __init__(self, duration, caster, target, mod, name):
        super().__init__(name, duration)
        self.amount = mod * caster.get_magic()

    def on_get_stat(self, value, stat_type):
        if stat_type == "magic":
            return value - self.amount if value - self.amount > 0 else 0
        return value


class AmplifyHeal(Effect):

    def __init__(self, duration, mod, name):
        super().__init__(name, duration)
        self.mod = mod

    def on_heal(self, battle, source, heal):
        return heal*self.mod


class Repel(Effect):

    def on_damage(self, battle, source, damage, damage_type):
        if damage_type in ("magic", "fire", "frost", "nature"):
            source.deal_damage(battle, source, damage, damage_type)
            self.remove()
            return 0
        return damage


class Share(Effect):

    def __init__(self, duration, caster, target, percentage, partner):
        super().__init__("sharing-pain", duration)
        self.percentage = percentage
        self.partner = caster

    def on_damage(self, battle, source, damage, damage_type):
        self.partner.deal_damage(battle, source, damage*self.percentage, damage_type)
        return damage*(1-self.percentage)


class Shield(Effect):

    def __init__(self, duration, caster, target,  name, percentage, amount=0):
        if amount:
            self.amount = amount
        else:
            self.amount = target.health*percentage

    def on_damage(self, battle, source, damage, damage_type):
        if amount >= damage:
            amount  -= damage
            damage = 0
        else:
            damage -= amount
            amount = 0
        if amount  <= 0:
            self.remove()
        return damage


class Repel(Effect):

    def on_damage(self, battle, source, damage, damage_type):
        if damage_type in ("magic", "fire", "frost", "nature"):
            source.deal_damage(battle, source, damage, damage_type)
            self.remove()
            return 0
        return damage


class BloodPact(Effect):

    def __init__(self, duration):
        super().__init__("blood-pact", duration)

    def on_start_turn(self, battle, character):
        if character.current_heal > 1:
            damage = charcter.current_health - round(character.current_heal * 0.75)
            if character.current_health - damage < 1:
                damage = character.current_health - 1
            character.deal_damage(battle, character, damage, "true")
        return (True, "%s has bleed for %d damage." % (character.name, ))

    def on_damage(self, battle, source, damage, damage_type):
        if damage_type == "true":
            return damage
        return damage*0.7

    def on_get_stat(self, value, stat_type):
        return value*1.5


class SwapDefense(Effect):

    def __init__(self, duration, caster, target):
        super().__init__("swap-defense", duration)
        self.target = target

    def on_get_stat(self, value, stat_type):
        if stat_type == "defense":
            return self.target.get_resist()
        elif stat_type == "resist":
            return self.target.get_defense()
        return value


class SwapAttack(Effect):

    def __init__(self, duration, caster, target):
        super().__init__("swap-attack", duration)
        self.target = target

    def on_get_stat(self, value, stat_type):
        if stat_type == "attack":
            return self.target.get_magic()
        elif stat_type == "magic":
            return self.target.get_attack()
        return value


class IncreaseStat(Effect):

    def __init__(self, duration, mod, stype, name):
        super().__init__(name, duration)
        self.mod = mod
        self.stype = stype

    def on_get_stat(self, value, stat_type):
        if self.stype == stat_type:
            return value * self.mod
        return value


class Combo(Effect):

    def __init__(self, duration, caster, target, spell, mod):
        super().__init__("melted", duration)
        self.caster = caster
        self.target = target
        self.spell = spell
        self.mod = mod
        self.counter = 1

    def on_damage(self, battle, source, damage, damage_type):
        if source == self.caster and self.spell == source.next_move.name:
            self.counter += 1
            return damage * self.mod ** self.counter
        elif source == self.caster:
            self.duration = 0
            return damage
        else:
            return damage


class Amplify(Effect):

    def __init__(self, duration, effect_type, mod, name):
        super().__init__(name, duration)
        self.mod = mod
        self.effect_type

    def on_damage(self, battle, source, damage, damage_type):
        if damage_type == self.effect_type:
            return damage * self.mod
        return damage

class AmplifyAll(Effect):

    def __init__(self, duration, mod, name):
        super().__init__(name, duration)

    def on_damage(self, battle, source, damage, damage_type):
        if damage_type == "true":
            return damage
        return damage * self.mod

class BoostSingle(Effect):

    def __init__(self, duration, stype, mod, name):
        super().__init__(name, duration)
        self.mod = mod
        self.stype = stype

    def on_get_stat(self, value, stat_type):
        if self.stype == stat_type:
            return value*self.mod
        return value


class LowerAccuracy(Effect):

    def __init__(self, duration, amount, name):
        super().__init__(name, duration)
        self.amount = amount

    def on_cast(self, battle, source, move):
        move.set_accuracy(move.accuracy-self.amount)


class HealOverTime(Effect):

    def __init__(self, duration, caster, target, percentage, scale):
        super().__init__("recovering", duration)
        self.amount = caster.get_magic()*percentage*scale

    def on_start_turn(self, battle, character):
        if character.fallen:
            return
        healing_done = character.apply_heal(battle, self.caster, self.amount)
        return (True, character.name + "healed for " + str(healing_done) + ".")


class SolarBeam(Effect):
    def __init__(self, duration, caster, target):
        super().__init__("solar-beam", duration)
        self.target = target
        self.caster = caster

    def on_start_turn(self, battle, character):
        dam = self.target.deal_damage(battle, self.caster, self.caster.get_magic() * 2, "nature")
        return (False, self.caster.name + " dealt " + str(dam) + " nature damage to " + self.target.name + ".\n")
