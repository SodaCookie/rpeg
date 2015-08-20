"""This module defines the Builder class"""

class Builder(object):
    """Builder class is base class for all builders."""

    def __init__(self, priority, key, value):
        """Builder takes a priority used to sort itself in the list
        of given builders, where 0 is the least important going to infinity,
        key used identify with builder should be given what value and value
        is the given value for building."""
        self.priority = priority
        self.key = key
        self.value = value

    def build_tag(self, tags):
        """Override if the builder defines how to build a tag"""
        return tag

    def build_name(self, template, tag):
        """Override if the builder defines how to build a name"""
        return template

    def build_stats(self, stats, tag):
        """Override if the builder defines how to build stats"""
        return stats

    def build_abilities(self, abilities, tag):
        """Override if the builder defines how to build abilities"""
        return abilities
