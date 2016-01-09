"""This module defines the Builder class"""

from xml.etree import ElementTree

def parse_names(filename, tag, rarity, speech):
    """Returns a list of viable names given tag, rarity and part of
    speech"""
    root = ElementTree.parse(filename).getroot()
    names = root.find(tag)
    return [node.text for node in names.findall("name[@rarity='%s'][@speech='%s']"%(rarity, speech))]

class Builder(object):
    """Builder class is base class for all builders."""

    NAME = "" # Override the name to detect builder

    def __init__(self, priority, value):
        """Builder takes a priority used to sort itself in the list
        of given builders, where 0 is the least important going to infinity,
        key used identify with builder should be given what value and value
        is the given value for building."""
        self.priority = priority
        self.value = value

    def build_tags(self, tags):
        """Override if the builder defines how to build a tag"""
        return tags

    def build_rarity(self, distribution):
        return distribution

    def build_types(self, types):
        """Override if the builder defines how to build a type"""
        return types

    def build_name(self, template, tag, rarity):
        """Override if the builder defines how to build a name"""
        return template

    def build_stats(self, stats, tag, rarity, type):
        """Override if the builder defines how to build stats"""
        return stats

    def build_abilities(self, abilities, tag):
        """Override if the builder defines how to build abilities"""
        return abilities

    def build_attributes(self, attributes, tag, rarity, type):
        return attributes
