from engine.game.item.builder import Builder
import os

class GeneralBuilder(Builder):
    """General purpose builder that is always called in the event
    that no parameters are called."""

    def __init__(self):
        super().__init__(0, "_general", None)

    def build_name(self, template, tag):
        return name