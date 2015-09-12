import pygame

from engine.ui.core.zone import Zone
from engine.ui.core.renderable import Renderable
from engine.ui.core.bindable import Bindable

class MoveIcon(Renderable, Bindable):
    """Move Icon is responsible for the casting of moves
    Move Icon can be given no move and it will display an empty
    move socket"""

    SLOTIMAGE = "image/ui/slot.png"
    HIGHLIGHTIMAGE = "image/ui/slot_highlight.png"
    DEFAULTICON = "image/icon/blank.png"

    def __init__(self, move, x, y):
        super(MoveIcon, self).__init__()
        self.move = move
        self.x = x
        self.y = y
        self.surface = self.draw(move)
        self.hover = self.draw_highlight(move)
        self.highlight = False

    @classmethod
    def draw(self, move):
        surface = pygame.image.load(MoveIcon.SLOTIMAGE).convert()
        surface = pygame.transform.scale(surface, (surface.get_width()*3, surface.get_height()*3))
        if move: # we draw the image on top
            # do some move blah blah....
            if move.icon: # if we have a given icon
                icon_image = pygame.image.load(move.icon).convert()
            else: # do a default icon
                icon_image = pygame.image.load(MoveIcon.DEFAULTICON).convert()
            icon_image = pygame.transform.scale(icon_image,
                (icon_image.get_width()*3, icon_image.get_height()*3))
            surface.blit(icon_image, (3, 3))
        return surface

    @classmethod
    def draw_highlight(self, move):
        surface = pygame.image.load(MoveIcon.HIGHLIGHTIMAGE).convert()
        surface = pygame.transform.scale(surface, (surface.get_width()*3, surface.get_height()*3))
        if move: # we draw the image on top
            # do some move blah blah....
            if move.icon: # if we have a given icon
                icon_image = pygame.image.load(move.icon).convert()
            else: # do a default icon
                icon_image = pygame.image.load(MoveIcon.DEFAULTICON).convert()
            icon_image = pygame.transform.scale(icon_image,
                (icon_image.get_width()*3, icon_image.get_height()*3))
            surface.blit(icon_image, (3, 3))
        return surface

    def render(self, surface, game):
        if self.bound and self.move:
            if self.bound.state == Zone.HOVERED:
                surface.blit(self.hover, (self.x, self.y))
            else:
                surface.blit(self.surface, (self.x, self.y))
        else:
            surface.blit(self.surface, (self.x, self.y))