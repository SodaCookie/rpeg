import pygame

from engine.ui.core.zone import Zone
from engine.ui.core.renderable import Renderable
from engine.ui.core.bindable import Bindable

class Slot(Renderable, Bindable):
    """Generic slot element that holds some value of type item or move.
    Once instantiated, the slot is immutable in type."""

    SLOTIMAGE = "image/ui/slot.png"
    HIGHLIGHTIMAGE = "image/ui/slot_highlight.png"
    DEFAULTICON = "image/icon/blank.png"

    def __init__(self, value, type_, x, y):
        # check if value is of the same type as type

        super().__init__()
        self.value = value
        self.type = type_
        self.x = x
        self.y = y
        self.surface = self.draw(value)
        self.hover = self.draw_highlight(value)
        self.highlight = False


    @classmethod
    def draw(self, value):
        surface = pygame.image.load(Slot.SLOTIMAGE).convert()
        surface = pygame.transform.scale(surface, (surface.get_width()*3, surface.get_height()*3))
        if value: # we draw the image on top
            # do some move blah blah....
            if value.icon: # if we have a given icon
                icon_image = pygame.image.load(value.icon).convert()
            else: # do a default icon
                icon_image = pygame.image.load(Slot.DEFAULTICON).convert()
            icon_image = pygame.transform.scale(icon_image,
                (icon_image.get_width()*3, icon_image.get_height()*3))
            surface.blit(icon_image, (3, 3))
        return surface

    @classmethod
    def draw_highlight(self, value):
        surface = pygame.image.load(Slot.HIGHLIGHTIMAGE).convert()
        surface = pygame.transform.scale(surface, (surface.get_width()*3, surface.get_height()*3))
        if value: # we draw the image on top
            # do some move blah blah....
            if value.icon: # if we have a given icon
                icon_image = pygame.image.load(value.icon).convert()
            else: # do a default icon
                icon_image = pygame.image.load(Slot.DEFAULTICON).convert()
            icon_image = pygame.transform.scale(icon_image,
                (icon_image.get_width()*3, icon_image.get_height()*3))
            surface.blit(icon_image, (3, 3))
        return surface

    @staticmethod
    def on_click(slot, game):
        if slot.value:
            game.current_object = slot.value
            game.current_hover = slot.surface
            game.current_slot = slot

            slot.value = None
            slot.surface = slot.draw(slot.value)
            slot.hover = slot.draw_highlight(slot.value)


    @staticmethod
    def off_click(slot, game):
        if (type(game.current_object) is slot.type) and not slot.value:
            slot.value = game.current_object
            game.current_hover = None
            game.current_object = None
            game.current_slot = None

            slot.surface = slot.draw(slot.value)
            slot.hover = slot.draw_highlight(slot.value)

    def render(self, surface, game):
        if self.bound and self.value:
            if self.bound.state == Zone.HOVERED:
                surface.blit(self.hover, (self.x, self.y))
            else:
                surface.blit(self.surface, (self.x, self.y))
        else:
            surface.blit(self.surface, (self.x, self.y))