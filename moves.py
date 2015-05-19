import random
import effects
import types
import constants
import itertools

class Move(object):

    def __init__(self, name, **kwargs):
        if type(name) == str:
            self.name = name
            self.prev = None
        elif issubclass(type(name), Move):
            self.name = name.name
            self.prev = name
        self.caster = None
        self.accuracy = 100
        self.crit = 0
        self.msg = ""
        self.target = None
        for key in kwargs.keys():
            if key == "accuracy":
                self.accuracy = kwargs[key]
            elif key == "crit":
                self.crit = kwargs[key]
        self.cur_accuracy = self.accuracy
        self.cur_crit = self.crit

    def set_caster(self, caster):
        self.caster = caster
        if self.prev:
            self.prev.set_caster(caster)

    def get_target(self, *args):
        target = None
        if len(args) <= 1: # No argument was given
            target = args[0].monster
            return target
        else:
            if args[1] == "monster":
                target = args[0].monster
                return target
            else:
                for member in args[0].party:
                    if args[1] == member.name:
                        target = member
                        return target
        return target

    def set_crit(self, crit):
        self.cur_crit = crit

    def set_accuracy(self, accuracy):
        self.cur_accuracy = accuracy

    def message(self, msg):
        self.msg += msg

    def get_message(self):
        if self.prev:
            self.msg = self.prev.get_message() + "\n" + self.msg
        return self.msg

    def cast(self, *args):
        self.msg = ""
        self.target = self.get_target(*args)
        if self.prev:
            self.prev.cast(*args)
        if random.randint(0, 99) <= self.cur_accuracy:  # accuracy roll
            if random.randint(0, 99) < self.cur_crit:  # crit roll
                self._crit(*args)
            else:
                self._cast(*args)
        else:
            self._miss(*args)
        self.cur_accuracy = self.accuracy
        self.cur_crit = self.crit

    def _crit(self, *args):
        """Override when wanting to make crit effect"""
        self._cast(*args)

    def _miss(self, *args):
        """Override when want to make a miss effect"""
        self.message(self.name.replace("-", " ").title() + " failed.")

    def _cast(self, *args):
        """Override to create effects"""
        pass


class SelfMove(Move):

    def get_target(self, *args):
       return self.caster


class SelfDefaultMove(Move):

    def get_target(self, *args):
        target = None
        if len(args) <= 1: # No argument was given
            self.target = self.caster
            return target
        else:
            if args[1] == "monster":
                target = args[0].monster
                return target
            else:
                for member in args[0].party:
                    if args[1] == member.name:
                        target = member
                        return target
        return target


class RemoveEffect(Move):

    def __init__(self, name, amount=1, enames=[], **kwargs):
        super().__init__(name, **kwargs)
        self.amount = amount
        self.enames = enames

    def _cast(self, *args):
        if self.target:
            if len(self.enames) == 0: # remove any move
                if self.amount > 0: # finite
                    for i in range(self.amount):
                        self.target.remove_last_effect()
                else: # remove all
                    self.target.effects = []
            else: # we have a list of effecst to remove
                if self.amount > 0:
                    count = 0
                    for cur_effect in self.enames:
                        while count < self.amount and self.target.has_effect(cur_effect):
                            self.target.remove_effect(cur_effect)
                            count += 1
                        if count >= self.amount:
                            break
                else:
                    for cur_effect in self.enames:
                        while self.target.has_effect(cur_effect):
                            self.target.remove_effect(cur_effect)
        else:
            self.message("Couldn't find a target.")

class PartyMove(Move):

    def get_target(self, *args):
        return args[0].party


class RandomPartyMove(Move):

    def get_target(self, *args):
        return random.choice(args[0].party)


class Mimic(Move):

    def _cast(self, *args):
        if self.target:
            self.target.next_move.cast(*args)
        else:
            self.message("Couldn't find a target.")


class CastDynamicEffect(Move):  # Dynamic effects get the castor's and target's stats past on to them

    def __init__(self, name, effect, duration, text="", *args, **kwargs):
        super().__init__(name, **kwargs)
        self.effect = effect
        self.text = text  # To be displaced when sucessful cast
        self.duration = duration
        self.args = args

    def _cast(self, *args):
        if self.target:
            tmp_effect = self.effect(self.duration, self.caster, self.target, *self.args)
            self.target.add_effect(tmp_effect)
            text = self.text.replace("[caster]", self.caster.name)
            text = text.replace("[target]", self.target.name)
            self.message(text)
        else:
            self.message("Couldn't find a target.")


class CastEffect(Move):

    def __init__(self, name, effect, duration, text="", *args, **kwargs):
        super().__init__(name, **kwargs)
        self.effect = effect
        self.text = text  # To be displaced when sucessful cast
        self.duration = duration
        self.args = args

    def _cast(self, *args):
        if self.target:
            tmp_effect = self.effect(self.duration, *self.args)
            self.target.add_effect(tmp_effect)
            text = self.text.replace("[caster]", self.caster.name)
            text = text.replace("[target]", self.target.name)
            self.message(text)
        else:
            self.message("Couldn't find a target.")


class Damage(Move):

    def __init__(self, name, dtype="physical", scale=1, **kwargs):
        super().__init__(name, **kwargs)
        self.dtype = dtype
        self.scale = scale

    def _cast(self, *args):
        if self.target:
            damage_dealt = self.target.deal_damage(args[0], self.caster, self.scale*self.caster.get_attack(), self.dtype)
            self.message(self.caster.name + " dealt " + str(damage_dealt) + " to " + self.target.name + ".")
        else:
            self.message("Couldn't find a target.")

    def _crit(self, *args):
        if self.target:
            damage_dealt = self.target.deal_damage(args[0], self.caster, 2*self.scale*self.caster.get_attack(), self.dtype)
            self.message("Critical hit!\n")
            self.message(self.caster.name + " dealt " + str(damage_dealt) + " to " + self.target.name + ".")
        else:
            self.message("Couldn't find a target.")


class BonusCritDamage(Damage):

    def __init__(self, name, dtype="physical", scale=1, bonus_crit=2.5):
        super(BonusCritDamage, self).__init__()
        self.arg = arg


class Heal(Move):

    def __init__(self, name, percentage, scale=1, **kwargs):
        super().__init__(name, **kwargs)
        self.percentage = percentage
        self.scale = scale

    def _cast(self, *args):
        if self.target:
            if self.target.fallen:
                self.message(self.target.name + " has fallen. Cannot be healed until revived.")
                return
            healing_done = self.target.apply_heal(args[0], self.caster, self.percentage*self.scale*self.caster.get_magic())
            self.message(self.target.name + " healed for " + str(healing_done) + ".")
        else:
            self.message("Couldn't find a target.")

class PercentHeal(Move):

    def __init__(self, name, percentage, **kwargs):
        super().__init__(name, **kwargs)
        self.percentage = percentage

    def _cast(self, *args):
        if self.target:
            if self.target.fallen:
                self.message(self.target.name + " has fallen. Cannot be healed until revived.")
                return
            healing_done = self.target.apply_heal(args[0], (self.target.heal-self.current_health)*self.percentage)
            self.message(self.target.name + " healed for " + str(healing_done) + ".")
        else:
            self.message("Couldn't find a target.")


class HealSelf(SelfMove, Heal):
    pass


class MagicDamage(Move):

    def __init__(self, name, dtype="magic", percentage=0.8, scale=1, **kwargs):
        super().__init__(name, **kwargs)
        self.dtype = dtype
        self.percentage = percentage
        self.scale = scale

    def _cast(self, *args):
        if self.target:
            damage_dealt = self.target.deal_damage(args[0], self.caster, self.scale*(self.caster.get_attack() * (1-self.percentage) + self.caster.get_magic() * self.percentage), self.dtype)
            self.message(self.caster.name + " dealt " + str(damage_dealt) + " " + self.dtype + " damage to " + self.target.name + ".")
        else:
            self.message("Couldn't find a target.")

    def _crit(self, *args):
        if self.target:
            damage_dealt = self.target.deal_damage(args[0], self.caster, 2*self.scale*(self.caster.get_attack() * (1-self.percentage) + self.caster.get_magic() * self.percentage), self.dtype)
            self.message("Critical hit!\n")
            self.message(self.caster.name + " dealt " + str(damage_dealt) + " " + self.dtype + " damage to " + self.target.name + ".")
        else:
            self.message("Couldn't find a target.")


class ScaleDamage(Move):

    def __init__(self, name, dtype="magic", stype="attack", percentage=0.8, scale=1, **kwargs):
        super().__init__(name, **kwargs)
        self.stype = stype # scale type
        self.dtype = dtype
        self.percentage = percentage
        self.scale = scale

    def _cast(self, *args):
        if self.target:
            if self.stype == "attack":
                scale = self.caster.get_attack() * constants.ATTACK_HEURISTIC
            elif self.stype == "defense":
                scale = self.caster.get_defense() * constants.DEFENSE_HEURISTIC
            elif self.stype == "health":
                scale = self.caster.health * constants.HEALTH_HEURISTIC
            elif self.stype == "magic":
                scale = self.caster.get_magic() * constants.MAGIC_HEURISTIC
            elif self.stype == "resist":
                scale = self.caster.get_resist() * constants.RESIST_HEURISTIC
            elif self.stype == "speed":
                scale = self.caster.get_speed() * constants.SPEED_HEURISTIC
            damage_dealt = self.target.deal_damage(args[0], self.caster, self.scale*(self.caster.get_attack() * (1-self.percentage) + scale * self.percentage), self.dtype)
            self.message(self.caster.name + " dealt " + str(damage_dealt) + " " + self.dtype + " damage to " + self.target.name + ".")
        else:
            self.message("Couldn't find a target.")

    def _crit(self, *args):
        if self.target:
            if self.stype == "attack":
                scale = self.caster.get_attack() * constants.ATTACK_HEURISTIC
            elif self.stype == "defense":
                scale = self.caster.get_defense() * constants.DEFENSE_HEURISTIC
            elif self.stype == "health":
                scale = self.caster.health * constants.HEALTH_HEURISTIC
            elif self.stype == "magic":
                scale = self.caster.get_magic() * constants.MAGIC_HEURISTIC
            elif self.stype == "resist":
                scale = self.caster.get_resist() * constants.RESIST_HEURISTIC
            elif self.stype == "speed":
                scale = self.caster.get_speed() * constants.SPEED_HEURISTIC
            damage_dealt = self.target.deal_damage(args[0], self.caster, 2*self.scale*(self.caster.get_attack() * (1-self.percentage) + scale * self.percentage), self.dtype)
            self.message("Critical hit!\n")
            self.message(self.caster.name + " dealt " + str(damage_dealt) + " " + self.dtype + " damage to " + self.target.name + ".")
        else:
            self.message("Couldn't find a target.")


class Compare(Move):

    def __init__(self, name, compare, move1, move2, **kwargs):
        super().__init__(name, **kwargs)
        self.move1 = move1
        self.move2 = move2
        self.compare = compare # if returns 1 then do the move1 else move 2
        self.last_move_cast = None

    def set_caster(self, caster):
        super().set_caster(caster)
        self.move1.set_caster(caster)
        self.move2.set_caster(caster)

    def get_message(self):
        return self.last_move_cast.get_message()

    def _cast(self, *args):
        if self.target:
            if hasattr(self.compare, "__call__"):
                if self.compare(self.caster, self.target):
                    self.move1.cast(*args)
                    self.last_move_cast = self.move1
                else:
                    self.move2.cast(*args)
                    self.last_move_cast = self.move2
            else:
                raise TypeError("'compare' object not callable")
        else:
            self.message("Couldn't find a target.")


class CastDynamicEffectParty(PartyMove, CastDynamicEffect):

    def _cast(self, *args):
        for member in self.target:
            tmp_effect = self.effect(self.duration, *self.args)
            member.add_effect(tmp_effect)
            text = self.text.replace("[caster]", self.caster.name)
            text = text.replace("[target]", member.name)
            self.message(text)


class DamageParty(PartyMove, Damage):

    def _cast(self, *args):
        for member in self.target:
            damage_dealt = member.deal_damage(args[0], self.caster, self.scale*self.caster.get_attack(), self.dtype)
            self.message(self.caster.name + " dealt " + str(damage_dealt) + " to " + member.name + ".")

    def _crit(self, *args):
        for member in self.target:
            damage_dealt = member.deal_damage(args[0], self.caster, 2*self.scale*self.caster.get_attack(), self.dtype)
            self.message("Critical hit!\n")
            self.message(self.caster.name + " dealt " + str(damage_dealt) + " to " + member.name + ".")


class MagicDamageParty(PartyMove, MagicDamage):

    def _cast(self, *args):
        for member in self.target:
            damage_dealt = member.deal_damage(args[0], self.caster, self.scale*(self.caster.get_attack() * (1-self.percentage) + self.caster.get_magic() * self.percentage), self.dtype)
            self.message(self.caster.name + " dealt " + str(damage_dealt) + " " + self.dtype + " damage to " + member.name + ".")

    def _crit(self, *args):
        for member in self.target:
            damage_dealt = member.deal_damage(args[0], self.caster, 2*self.scale*(self.caster.get_attack() * (1-self.percentage) + self.caster.get_magic() * self.percentage), self.dtype)
            self.message("Critical hit!\n")
            self.message(self.caster.name + " dealt " + str(damage_dealt) + " " + self.dtype + " damage to " + member.name + ".")


class Recoil(Move):

    def __init__(self, name, rdtype="physical", recoil=0.1, **kwargs):
        super().__init__(name, **kwargs)
        self.rdtype = rdtype  # Return damage type
        self.recoil = recoil

    def _cast(self, *args):
        damage_dealt = self.caster.deal_damage(args[0], self.caster, self.recoil*self.caster.get_attack(), self.rdtype)
        self.message(self.caster.name + " took " + str(damage_dealt) + " in recoil.")


class HealParty(PartyMove):

    def __init__(self, name, percentage, scale, **kwargs):
        super().__init__(name, **kwargs)
        self.percentage = percentage
        self.scale = scale

    def _cast(self, *args):
        for member in self.target:
            if self.target.fallen:
                self.message(self.target.name + " has fallen. Cannot be healed until revived.")
                continue
            healing_done = member.apply_heal(args[0], self.caster, self.percentage*self.scale*self.caster.get_magic())
            self.message(self.target.name + " healed for " + str(healing_done) + ".\n")


class RandomHeal(RandomPartyMove, Heal):
    pass


class Repeat(Move):

    def __init__(self, name, repeat, **kwargs):
        super().__init__(name, **kwargs)
        self.repeat = repeat

    def get_message(self):
        return self.msg[:-1]

    def _cast(self, *args):
        if self.prev:
            for i in range(self.repeat):
                self.prev.cast(*args)
                self.message(self.prev.get_message()+"\n")


class Message(Move):

    def __init__(self, name, text="", before=False, stop=False, **kwargs):
        super().__init__(name, **kwargs)
        self.text = text
        self.stop = stop # if true will cut out all messages placed before
        self.before = before # if true will place your message before the casts

    def get_message(self):
        if self.prev and not self.stop:
            if self.before:
                self.msg = self.msg + "\n" + self.prev.get_message()
            else:
                self.msg = self.prev.get_message() + "\n" + self.msg
        return self.msg

    def _cast(self, *args):
        text = self.text.replace("[caster]", self.caster.name)
        text = text.replace("[target]", self.target.name)
        self.message(text)


class CastEffectSelf(SelfMove, CastEffect):
    pass


class CastDynamicEffectSelf(SelfMove, CastDynamicEffect):
    pass


class MonsterDamage(Move):

    def _cast(self, *args):
        target = random.choice(args[0].party)
        damage_dealt = target.deal_damage(args[0], self.caster, self.caster.get_attack(), "physical")
        self.message(self.caster.name + " dealt " + str(damage_dealt) + " to " + target.name + ".")


if __name__ == "__main__":
    # Testing
    nmove = target_cast(damage(Move("test")))