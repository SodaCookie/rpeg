import random

from engine.system import Message
from engine.game.dungeon.action import Action
from engine.game.monster.monster import Monster

class BattleAction(Action):

    def __init__(self, challenge=5, monsters=None):
        """Initiate battle.
        challenge -> int
        monsters -> list str"""
        super().__init__()
        self.challenge = challenge
        self.monsters = monsters

    def execute(self, game, system):
        """Initiates a battle.
        If no monsters are declared for the battle then a random
        set of monsters will be generated at the specified challenge
        rating. Otherwise monsters will override."""
        monster_names = []
        if self.monsters:
            monster_names = self.monsters
        else:
            challenge = self.challenge
            while challenge > 0 and len(monster_names) < 3:
                valid_monsters = []
                # Get valid monsters
                for name, monster in Monster.MONSTERS.items():
                    if monster["rating"] <= challenge and \
                            monster["location"] == game.floor_type and \
                            not monster["unique"]:
                        valid_monsters.append((name, monster["rating"]))
                # If no valid monsters break
                if not valid_monsters:
                    break
                # Select monster
                name, rating = random.choice(valid_monsters)
                monster_names.append(name)
                challenge -= rating

            # If there are remaining challenge points to distribute
            if challenge: # Any rating left over
                          # then we add the highest
                valid_monsters = [(name, monster["rating"])
                    for name, monster in Monster.MONSTERS.items()
                    if monster["rating"] <= challenge and \
                    monster["location"] == game.floor_type and \
                    not monster["unique"]]

                highest_value = 0
                for name, value in valid_monsters:
                    if value > highest_value:
                        highest_value = value
                valid_names = [name for name, value in valid_monsters
                               if value <= highest_value]
                monster_names.append(random.choice(valid_names))

        # Execute
        system.message("battle", Message("start",
            [Monster(name) for name in monster_names]))
        system.message("ui", Message("layout", "battle"))
        system.message("sound", Message("bg", "data/sound/background/Theyre-Closing-In_looping.wav"))