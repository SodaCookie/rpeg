import character

class Player(Character):

    MAX_LEVEL = 15
    POINTS_PER_LEVEL = 10

    def __init__(self, name):
        self.name = name
        self.effects = []
        self.moves = []
        self.fallen = False
        self.drop = None  # tmp variable for dropped items
        self.args = []
        self.next_move = self.moves[0]
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

        self.experience = 0
        self.level = 1

        self.equipment = {}
        self.equipment["hand1"] = Item(generate=False)
        self.equipment["hand2"] = Item(generate=False)
        self.equipment["body"] = Item(generate=False)
        self.equipment["legs"] = Item(generate=False)
        self.equipment["feet"] = Item(generate=False)
        self.equipment["arms"] = Item(generate=False)
        self.equipment["head"] = Item(generate=False)
        self.equipment["extra1"] = Item(generate=False)
        self.equipment["extra2"] = Item(generate=False)

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
        self.current_health = self.health
        self.drop = None
        self.effects = []
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
        log = "%s uses %s:\n" % (self.name, self.next_move.name.replace("-", " ").title())
        self.next_move.cast(battle, *self.args)
        log += self.next_move.get_message()

        # Remove the effect after the duration is gone
        for effect in self.effects[:]:
            effect.duration -= 1
            if effect.duration <= 0:
                self.effects.remove(effect)
        self.args = []
        return log

    def deal_damage(self, battle, source, damage, damage_type):
        for effect in self.effects:
            damage = effect.on_damage(battle, source, damage, damage_type)
        damage = int(damage - self.get_defense() * (random.randint(100-DAMAGE_VARIATION, 100+DAMAGE_VARIATION)/100))
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
        heal = int(heal*(random.randint(100-HEAL_VARIATION, 100+HEAL_VARIATION)/100))
        if self.fallen:
            heal = 0
        if self.current_health + heal > self.health:
            self.current_health = self.health
        else:
            self.current_health += heal
        return heal

    def calculate_power(self):
         power = 0
         power += self.attack*ATTACK_HEURISTIC
         power += self.defense*DEFENSE_HEURISTIC
         power += self.magic*MAGIC_HEURISTIC
         power += self.health*HEALTH_HEURISTIC
         power += self.resist*RESIST_HEURISTIC
         power += self.speed*SPEED_HEURISTIC
         return power

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

    def give_experience(self, experience):
        if self.level < MAX_LEVEL:
            if self.level*100+experience > MAX_LEVEL*100:
                experience = (self.level*100+experience)-MAX_LEVEL*100
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

            gain_attack += round(attack_weight * POINTS_PER_LEVEL)
            gain_defense += round(defense_weight * POINTS_PER_LEVEL)
            gain_health += round(health_weight * POINTS_PER_LEVEL)
            gain_speed += round(speed_weight * POINTS_PER_LEVEL)
            gain_magic += round(magic_weight * POINTS_PER_LEVEL)
            gain_resist += round(resist_weight * POINTS_PER_LEVEL)

        self.base_attack += gain_attack
        self.base_defense += gain_defense
        self.base_health += gain_health
        self.base_speed += gain_speed
        self.base_magic += gain_magic
        self.base_resist += gain_resist

        return "You earned %d level(s)\n\
Attack: %d ----- +%d\n\
Defense: %d ----- +%d\n\
Health: %d ----- +%d\n\
Speed: %d ----- +%d\n\
Magic: %d ----- +%d\n\
Resist: %d ----- +%d\n\
You have %d skill point(s) to spend.\n\
Refer to help if you need help spending points." % (counter,\
        self.base_attack, gain_attack,\
        self.base_defense, gain_defense,\
        self.base_health, gain_health,\
        self.base_speed, gain_speed,\
        self.base_magic, gain_magic,\
        self.base_resist, gain_resist,\
        self.skill_points)

    def set_args(*args):
        self.args = args

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

    def get_equip(self, slot=""):
        if slot:
            try:
                return "%s ----- %s\n========================\n\
%s" % (slot, self.equipment[slot].name, self.equipment[slot].getStats())
            except IndexError:
                return "Slot %s not found." % slot
        else:
            return "Hand1 ----- %s\n\
Hand2 ----- %s\n\
Body ----- %s\n\
Legs ----- %s\n\
Feet ----- %s\n\
Arms ----- %s\n\
Head ----- %s\n\
Extra1 ----- %s\n\
Extra2 ----- %s\n" % \
            (self.equipment["hand1"].name.title(),\
             self.equipment["hand2"].name.title(),\
             self.equipment["body"].name.title(),\
             self.equipment["legs"].name.title(),\
             self.equipment["feet"].name.title(),\
             self.equipment["arms"].name.title(),\
             self.equipment["head"].name.title(),\
             self.equipment["extra1"].name.title(),\
             self.equipment["extra2"].name.title())

    def getStats(self):
        if self.get_level() == MAX_LEVEL:
            experience = 100
        else:
            experience = self.experience
        return ' | EXP: %d/100 | LVL %d\n========================\nAttack: %d\nDefense: %d\nHealth: %d\\%d\nSpeed: %d\nMagic: %d\nResist: %d'\
     % (experience, self.get_level(), self.attack, self.defense, self.current_health, self.health, self.speed, self.magic, self.resist)