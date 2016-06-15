import pygame

from engine.system import Message

from engine.ui.element.abstractslot import AbstractSlot

class ItemSlot(AbstractSlot):

    SLOTIMAGE = "image/ui/slot.png"
    HIGHLIGHTIMAGE = "image/ui/slot_highlight.png"
    DEFAULTICON = "image/icon/blank.png"

    def __init__(self, name, x, y, itemslot, address, on_change=None):
        super().__init__(name, (x, y, 54, 54), "item", address,
            cloneable = False,
            dropable = False,
            swapable = True)
        self.itemslot = itemslot
        if on_change is not None:
            self.on_change = on_change

    def on_dropped(self, game, system):
        system.message("sound", Message("ui", "data/sound/drop-off.wav"))

    def on_setted(self, game, system):
        system.message("sound", Message("ui", "data/sound/pick-up.wav"))

    def on_drop(self, obj):
        """Returns True if the dropped item's slot and itemslot is the same."""
        # NotImplemented
        return True

    def render_neutral(self, game):
        surface = pygame.image.load(ItemSlot.SLOTIMAGE).convert()
        surface = pygame.transform.scale(surface, (surface.get_width()*3, surface.get_height()*3))
        if self.value: # we draw the image on top
            if self.value.icon: # if we have a given icon
                icon_image = pygame.image.load(self.value.icon).convert()
            else: # do a default icon
                icon_image = pygame.image.load(ItemSlot.DEFAULTICON).convert()
            icon_image = pygame.transform.scale(icon_image,
                (icon_image.get_width()*3, icon_image.get_height()*3))
            surface.blit(icon_image, (3, 3))
        return surface

    def render_hover(self, game):
        """Draw method when highlighted"""
        surface = pygame.image.load(ItemSlot.HIGHLIGHTIMAGE).convert()
        surface = pygame.transform.scale(surface, (surface.get_width()*3, surface.get_height()*3))
        if self.value: # we draw the image on top
            # do some move blah blah....
            if self.value.icon: # if we have a given icon
                icon_image = pygame.image.load(self.value.icon).convert()
            else: # do a default icon
                icon_image = pygame.image.load(ItemSlot.DEFAULTICON).convert()
            icon_image = pygame.transform.scale(icon_image,
                (icon_image.get_width()*3, icon_image.get_height()*3))
            surface.blit(icon_image, (3, 3))
        return surface

    def render_clicked(self, game):
        surface = pygame.image.load(ItemSlot.SLOTIMAGE).convert()
        surface = pygame.transform.scale(surface, (surface.get_width()*3, surface.get_height()*3))
        if self.cloneable and self.value:
            if self.value.icon: # if we have a given icon
                icon_image = pygame.image.load(self.value.icon).convert()
            else: # do a default icon
                icon_image = pygame.image.load(ItemSlot.DEFAULTICON).convert()
            icon_image = pygame.transform.scale(icon_image,
                (icon_image.get_width()*3, icon_image.get_height()*3))
            surface.blit(icon_image, (3, 3))
        return surface