"""This module defines the Builder class for Monsters"""

from xml.etree import ElementTree

def parse_names(filename, tag, rank, speech):
    """returns a list of viable names given tag, rank and part of
    speech"""
    root = ElementTree.parse(filename).getroot()
    names = root.find("names").find(tag)
    # print(rank, speech)
    return [node.text for node in names.findall("name[@rank='%s'][@speech='%s']"%(rank, speech))]

class Builder(object):
    """Builder class is base class for monster builders."""

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

    def build_rank(self, distribution): # common, elite, boss monster
        """Override if the builder defines how to build a rank"""
        return distribution

    def build_type(self, types): # type of monster
        """Override if the builder defines how to build a type"""
        return types

    def build_name(self, template, tag, rank, type):
        """Override if the builder defines how to build a name"""
        return template

    def build_stats(self, distribution, tag, rank, type):
        """Override if the builder defines how to build stats"""
        return distribution

    def build_abilities(self, abilities, tag, rank, type):
        """Override if the builder defines how to build abilities"""
        return abilities