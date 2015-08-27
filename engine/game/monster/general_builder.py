import random
import os

from engine.game.monster.builder import Builder, parse_names


class GeneralBuilder(Builder):
    """General purpose builder that is always called in the event
    that no parameters are called."""

    NAME = "_general"

    def __init__(self, parameter):
        super().__init__(0, None)

    def build_name(self, template, tag, rank, type):
        """Reads from XML file the possible words to fill in a given template"""
        for key in template:
            replacement = parse_names(os.path.dirname(os.path.realpath(__file__))+"/data/monster.xml", tag, rank, key)
            template[key] = random.choice(replacement)
        return template