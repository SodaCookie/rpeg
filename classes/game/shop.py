import objects.item as item
from random import triangular, choice, uniform

class Shop(object):

    # rarity is as follows
    # common - 0
    # rare - 1
    # epic - 2
    # legendary - 3
    # Max of 5 items until we have scroll
    RARITY = ["common", "rare", "epic", "legendary"]
    SHOP_NAMES = ["The Rat's Cellar",
                  "Ye Old Storage",
                  "Dank Mimi's Shop",
                  "Lord of Items"]
    PRICE_POINT_VARIATION = 1.4

    def __init__(self, power, name="", num_items="5",
                 price_point="normal", rarity="1"):
        # create items
        self.items = []
        num_items = int(num_items)
        rarity = int(rarity)

        for i in range(num_items):
            rarity_roll = round(triangular(1, 4, rarity))
            assert 1 <= rarity_roll <= 4, "Rarity: %d" % rarity_roll
            rolled_rarity = Shop.RARITY[rarity_roll-1]
            tmp_item = item.Item(power, rolled_rarity)
            value = round(tmp_item.get_value()*uniform(0.95, 1.05))
            if price_point == "high":
                value = value * Shop.PRICE_POINT_VARIATION
            elif price_point == "normal":
                pass
            elif price_point == "low":
                value = value * PRICE_POINT_VARIATION
            self.items.append((tmp_item, value))

        if name:
            self.name = name.replace("_", " ")
        else:
            self.name = choice(Shop.SHOP_NAMES)