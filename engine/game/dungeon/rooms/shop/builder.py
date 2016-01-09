def parse_shopnames(filename):
    """Parses possible shop names from a data file"""
    with open(filename, 'r') as file:
        names = file.read().split('\n')
    return names


class Builder(object):
    """Builder class is base class for all shop builders."""

    NAME = "" # Override the name to detect builder

    def __init__(self, priority, value):
        """Builder takes a priority used to sort itself in the list
        of given builders, where 0 is the least important going to infinity,
        key used identify with builder should be given what value and value
        is the given value for building."""
        self.priority = priority
        self.value = value

    def build_items(self, items):
        """Override to give items"""
        return items

    def build_name(self, name):
        """Override to give name"""
        return name