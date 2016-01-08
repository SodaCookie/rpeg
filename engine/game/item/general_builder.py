from engine.game.item.builder import Builder, parse_names
import os
import random

class GeneralBuilder(Builder):
    """General purpose builder that is always called in the event
    that no parameters are called."""

    NAME = "_general"

    def __init__(self, parameter):
        super().__init__(0, None)

    def build_name(self, template, tag, rarity):
        for key, words in template.items():
            speech, count = key
            replacements = parse_names(os.path.dirname(os.path.realpath(__file__))+"/data/names.xml", tag, rarity, speech)
            for i in range(count):
                words[i] = random.choice(replacements)
        return template