import pygame

from engine.ui.core.renderable import Renderable
from engine.ui.core.bindable import Bindable

class MoveIcon(Renderable, Bindable):
    """Move Icon is responsible for the casting of moves
    Move Icon can be given no move and it will display an empty
    move socket"""

    SLOTIMAGE = "image/ui/slot.png"

    def __init__(self, move, x, y):
        super(MoveIcon, self).__init__()
        self.move = move
        self.x = x
        self.y = y
        self.surface = self.draw(move)

    def draw(self, move):
        surface = pygame.image.load(MoveIcon.SLOTIMAGE).convert()
        surface = pygame.transform.scale(surface, (surface.get_width()*3, surface.get_height()*3))
        if move: # we draw the image on top
            # do some move blah blah....
            pass
        return surface

    def render(self, surface, game):
        surface.blit(self.surface, (self.x, self.y))