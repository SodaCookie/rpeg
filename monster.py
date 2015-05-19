import character

class Monster(character.Character):

    def __init__(self, power, difficulty = 1, mtype=""):
        super().__init__("")
        self.difficulty = difficulty
        self.monster = monster
        self.monstertype = mtype
        self.attack = 0
        self.defense = 0
        self.resist = 0
        self.magic = 0
        self.current_health = 0
        self.health = 0
        self.speed = 0
        self.power = power
        with open("prefix.txt", "r") as f:
            self.prefix = f.read().split("\n")
        with open("monster.txt", "r") as f:
            self.monster = f.read().split("\n")
        with open("suffix.txt", "r") as f:
            self.suffix = f.read().split("\n")

        # if power == 0:
        #     power = 0
        #     for p in party:
        #         power += p.attack + p.defense + p.health + p.magic + p.speed
        #     power /= len(party)

        self.generateName()
        self.generateStats(power)

    def randCoef(self, min, max):
        return random.random() * (max - min) + min

    def generateStats(self, power):
        """Generates stats based on the power level of the players"""
        pass

    def generateName(self):
        choices = {}
        if self.monstertype == "":
            choices["monster"] = random.choice(self.monster)
        else:
            # Placeholder. If specified monster type
            choices["monster"] = self.monster
        if self.difficulty >= 2:
            choices["prefix"] = random.choice(self.prefix)
        if self.difficulty >= 3:
            choices["suffix"] = random.choice(self.suffix)

        if self.difficulty == 1:
            self.name = "%(monster)s" % (choices)
        elif self.difficulty == 2:
            self.name = "%(prefix)s %(monster)s" % (choices)
        elif self.difficulty == 3:
            self.name = "%(prefix)s %(monster)s of %(suffix)s" % (choices)