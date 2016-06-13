from engine.ui.core.manager import Manager

import engine.ui.element as element
from engine.ui.draw.simple import draw_rect

class PartyManager(Manager):

    def __init__(self, x, y):
        super().__init__("party", x, y)
        self.add_renderable(element.CharacterCard("Character1", self.x, self.y, 0))
        self.add_renderable(element.CharacterCard("Character2", self.x + 312, self.y, 1))
        self.add_renderable(element.CharacterCard("Character3", self.x + 624, self.y, 2))
        self.add_renderable(element.CharacterCard("Character4", self.x + 936, self.y, 3))
