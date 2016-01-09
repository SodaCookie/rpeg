from engine.game.dungeon.rooms.shop.general_builder import GeneralBuilder

class Shop(object):
    """Holds items for sale in a given shop room"""

    BUILDERS = [GeneralBuilder]

    def __init__(self, **parameters):
        # create items
        self.builders = [] # construct builders
        for builder in Shop.BUILDERS:
            value = parameters.get(builder.NAME)
            self.builders.append(builder(value))
        self.builders = sorted(self.builders, key=lambda b: b.priority)

        self.name = self._generate_name()
        self.itemtable = self._generate_items() # hash of item to values

    def _generate_name(self):
        """Invokes all the builders' build_name method"""
        name = ""
        for builder in self.builders:
            name = builder.build_name(name)
        return name

    def _generate_items(self):
        """Invokes all the builders' build_items method"""
        items = {}
        for builder in self.builders:
            items = builder.build_items(items)
        return items

if __name__ == "__main__":
    s = Shop()
    print(s.name)
    for item, value in s.itemtable.items():
        print(item.name, ":", value)