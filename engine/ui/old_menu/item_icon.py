import pygame

from engine.ui.core.zone import Zone
from engine.ui.core.renderable import Renderable
from engine.ui.core.bindable import Bindable

class ItemIcon(Renderable, Bindable):
    """Item Icon is responsible for rendering items and slots
    in inventory and other menus"""

    SLOTIMAGE = "image/ui/slot.png"
    HIGHLIGHTIMAGE = "image/ui/slot_highlight.png"
    DEFAULTICON = "image/icon/blank.png"

    def __init__(self, item, x, y):
        super().__init__()
        self.item = item
        self.x = x
        self.y = y
        self.surface = self.draw(item)
        self.hover = self.draw_highlight(item)
        self.highlight = False

    @classmethod
    def draw(self, item):
        surface = pygame.image.load(ItemIcon.SLOTIMAGE).convert()
        surface = pygame.transform.scale(surface, (surface.get_width()*3, surface.get_height()*3))
        if item: # we draw the image on top
            # do some move blah blah....
            if item.icon: # if we have a given icon
                icon_image = pygame.image.load(item.icon).convert()
            else: # do a default icon
                icon_image = pygame.image.load(ItemIcon.DEFAULTICON).convert()
            icon_image = pygame.transform.scale(icon_image,
                (icon_image.get_width()*3, icon_image.get_height()*3))
            surface.blit(icon_image, (3, 3))
        return surface

    @classmethod
    def draw_highlight(self, item):
        surface = pygame.image.load(ItemIcon.HIGHLIGHTIMAGE).convert()
        surface = pygame.transform.scale(surface, (surface.get_width()*3, surface.get_height()*3))
        if item: # we draw the image on top
            # do some move blah blah....
            if item.icon: # if we have a given icon
                icon_image = pygame.image.load(item.icon).convert()
            else: # do a default icon
                icon_image = pygame.image.load(ItemIcon.DEFAULTICON).convert()
            icon_image = pygame.transform.scale(icon_image,
                (icon_image.get_width()*3, icon_image.get_height()*3))
            surface.blit(icon_image, (3, 3))
        return surface

    def render(self, surface, game):
        if self.bound and self.item:
            if self.bound.state == Zone.HOVERED:
                surface.blit(self.hover, (self.x, self.y))
            else:
                surface.blit(self.surface, (self.x, self.y))
        else:
            surface.blit(self.surface, (self.x, self.y))