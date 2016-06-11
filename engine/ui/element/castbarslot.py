import pygame

from engine.ui.element.abstractslot import AbstractSlot

class CastBarSlot(AbstractSlot):

    SLOTIMAGE = "image/ui/slot.png"
    HIGHLIGHTIMAGE = "image/ui/slot_highlight.png"
    DEFAULTICON = "image/icon/blank.png"

    def __init__(self, name, x, y, address):
        super().__init__(name, (x, y, 54, 54), "item", address,
            cloneable = False,
            dropable = True,
            swapable = True)

    def on_drop(self, obj):
        """Returns True if the dropped item's slot and itemslot is the same."""
        # NotImplemented
        return True

    def on_set(self, game):
        if game.encounter:
            return False
        return True

    def on_change(self, game, system):
        pass

    def render_neutral(self, game):
        surface = pygame.image.load(self.SLOTIMAGE).convert()
        surface = pygame.transform.scale(surface, (surface.get_width()*3, surface.get_height()*3))
        if self.value: # we draw the image on top
            if self.value.icon: # if we have a given icon
                icon_image = pygame.image.load(self.value.icon).convert()
            else: # do a default icon
                icon_image = pygame.image.load(self.DEFAULTICON).convert()
            icon_image = pygame.transform.scale(icon_image,
                (icon_image.get_width()*3, icon_image.get_height()*3))
            surface.blit(icon_image, (3, 3))
        return surface

    def render_hover(self, game):
        """Draw method when highlighted"""
        surface = pygame.image.load(self.HIGHLIGHTIMAGE).convert()
        surface = pygame.transform.scale(surface, (surface.get_width()*3, surface.get_height()*3))
        if self.value: # we draw the image on top
            # do some move blah blah....
            if self.value.icon: # if we have a given icon
                icon_image = pygame.image.load(self.value.icon).convert()
            else: # do a default icon
                icon_image = pygame.image.load(self.DEFAULTICON).convert()
            icon_image = pygame.transform.scale(icon_image,
                (icon_image.get_width()*3, icon_image.get_height()*3))
            surface.blit(icon_image, (3, 3))
        return surface

    def render_clicked(self, game):
        surface = pygame.image.load(self.SLOTIMAGE).convert()
        surface = pygame.transform.scale(surface, (surface.get_width()*3, surface.get_height()*3))
        if self.value:
            if self.value.icon: # if we have a given icon
                icon_image = pygame.image.load(self.value.icon).convert()
            else: # do a default icon
                icon_image = pygame.image.load(self.DEFAULTICON).convert()
            icon_image = pygame.transform.scale(icon_image,
                (icon_image.get_width()*3, icon_image.get_height()*3))
            surface.blit(icon_image, (3, 3))
        return surface