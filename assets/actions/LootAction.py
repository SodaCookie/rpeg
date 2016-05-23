from engine.game.dungeon.action import Action
from engine.game.item.item_factory import ItemFactory

class LootAction(Action):
    LOW = "low"
    MEDUIM = "medium"
    HIGH = "high"

    def __init__(self, reward_tier="low", shards=None, items=None):
        """Reward player.
        reward_tier -> str
        shards -> int
        items -> list str"""
        super().__init__()
        self.reward_tier = reward_tier
        self.shards = shards
        self.items = items

    def execute(self, game):
        """Creates a loot table
        If shard or items is declared the respective loot will be created.
        Otherwise reward_tier will override generating a random loot table."""

        shards = 0
        items = []

        # Handle no shards or items
        if not self.shards and not self.items:
            # Generate shards
            if self.reward_tier == Loot.LOW:
                shards = game.floor_level * random.randint(15, 20)
            elif self.reward_tier == Loot.MEDUIM:
                shards = game.floor_level * random.randint(30, 35)
            elif self.reward_tier == Loot.HIGH:
                shards = game.floor_level * random.randint(50, 70)

            # Generate items
            if self.reward_tier == Loot.MEDUIM:
                # 30% change of getting an item of "medium" reward tier
                if random.randint(0, 99) < 30:
                    self.items = [ItemFactory.generate(
                        game.encounter, game.floor_type)]
            elif self.reward_tier == Loot.HIGH:
                # 70% change of getting an item of "high" reward tier
                if random.randint(0, 99) < 70:
                    self.items = [ItemFactory.generate(
                        game.encounter, game.floor_type)]

        else:
            if self.shards:
                shards = self.shards
            if self.items:
                items = [ItemFactory.static_generate(name)
                    for name in self.items]

        # Assign create loot table to the game
        game.loot = (shards, items)
        game.party.add_shards(shards)
        game.focus_window = "loot"